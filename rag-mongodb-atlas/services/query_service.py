"""
Servicio para traducir lenguaje natural a consultas MongoDB
"""
from typing import Dict, List, Any
import json
from bson import json_util
from datetime import datetime
from services.llm_service import LLMService
from config.database import mongodb

class QueryService:
    """Servicio de consultas en lenguaje natural"""

    def __init__(self):
        self.llm_service = LLMService()

    async def natural_language_query(self, question: str) -> Dict[str, Any]:
        """
        Traduce una pregunta en lenguaje natural a una consulta MongoDB y la ejecuta

        Args:
            question: Pregunta del usuario en lenguaje natural

        Returns:
            Dict con la respuesta y los datos consultados
        """

        # Obtener esquema de las colecciones
        schema_info = await self._get_database_schema()

        # Prompt para el LLM
        prompt = f"""Eres un asistente experto en MongoDB que traduce preguntas en lenguaje natural a consultas MongoDB y genera respuestas claras.

ESQUEMA DE BASE DE DATOS:
{schema_info}

PREGUNTA DEL USUARIO:
{question}

INSTRUCCIONES:
1. Analiza la pregunta y determina qué colección(es) consultar
2. Genera la consulta MongoDB apropiada (find, aggregate, count, etc.)
3. La consulta debe ser un objeto JSON válido
4. Devuelve tu respuesta en el siguiente formato JSON:

{{
    "collection": "nombre_de_coleccion",
    "operation": "find|aggregate|count_documents",
    "query": {{}},
    "projection": {{}},
    "limit": 10,
    "explanation": "Explicación breve de qué datos se están consultando"
}}

EJEMPLOS:
Pregunta: "¿Cuántos clientes tengo activos?"
Respuesta: {{"collection": "clientes", "operation": "count_documents", "query": {{"estado": "activo"}}, "explanation": "Contando clientes con estado activo"}}

Pregunta: "Muéstrame los productos con bajo stock"
Respuesta: {{"collection": "productos", "operation": "find", "query": {{"estado": "bajo_stock"}}, "limit": 10, "explanation": "Buscando productos con stock bajo"}}

Pregunta: "¿Cuál es el total de ventas de marzo?"
Respuesta: {{"collection": "ventas", "operation": "aggregate", "query": [{{"$match": {{"fecha": {{"$regex": "^2024-03"}}}}}}, {{"$group": {{"_id": null, "total": {{"$sum": "$total"}}}}}}], "explanation": "Sumando el total de todas las ventas de marzo 2024"}}

Ahora responde con el JSON para la pregunta del usuario."""

        try:
            # Obtener respuesta del LLM
            llm_response = self.llm_service.generate_response(prompt, temperature=0.3)

            # Parsear la respuesta JSON
            # Extraer JSON del texto (puede venir con markdown)
            response_text = llm_response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            query_plan = json.loads(response_text)

            # Ejecutar la consulta
            results = await self._execute_query(query_plan)

            # Generar respuesta en lenguaje natural
            natural_response = await self._generate_natural_response(
                question, query_plan, results
            )

            return {
                "question": question,
                "query_plan": query_plan,
                "results": results,
                "answer": natural_response,
                "count": len(results) if isinstance(results, list) else results
            }

        except Exception as e:
            print(f"Error en consulta natural: {e}")
            return {
                "question": question,
                "error": str(e),
                "answer": f"Lo siento, hubo un error al procesar tu consulta: {str(e)}"
            }

    async def _get_database_schema(self) -> str:
        """Obtiene información del esquema de la base de datos dinámicamente"""

        db = mongodb.db
        schema_parts = ["COLECCIONES DISPONIBLES:\n"]

        # Obtener todas las colecciones
        collection_names = await db.list_collection_names()

        for idx, coll_name in enumerate(collection_names, 1):
            collection = mongodb.get_collection(coll_name)

            # Obtener documento de muestra para inferir campos
            sample = await collection.find_one({})

            schema_parts.append(f"\n{idx}. {coll_name}:")

            if sample:
                for key, value in sample.items():
                    if key != '_id':
                        field_type = type(value).__name__
                        schema_parts.append(f"   - {key} ({field_type})")
            else:
                schema_parts.append("   (Colección vacía)")

        return "\n".join(schema_parts)

    async def _execute_query(self, query_plan: Dict) -> Any:
        """Ejecuta la consulta MongoDB"""

        collection_name = query_plan.get("collection")
        operation = query_plan.get("operation", "find")
        query = query_plan.get("query", {})
        projection = query_plan.get("projection")
        limit = query_plan.get("limit", 20)

        collection = mongodb.get_collection(collection_name)

        if operation == "find":
            cursor = collection.find(query, projection)
            if limit:
                cursor = cursor.limit(limit)
            results = await cursor.to_list(length=limit)

            # Convertir ObjectId y datetime a string
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
                # Convertir datetime a ISO string
                for key, value in list(doc.items()):
                    if isinstance(value, datetime):
                        doc[key] = value.isoformat()

            return results

        elif operation == "count_documents":
            count = await collection.count_documents(query)
            return count

        elif operation == "aggregate":
            cursor = collection.aggregate(query)  # query es el pipeline
            results = await cursor.to_list(length=100)

            # Convertir ObjectId y datetime a string
            for doc in results:
                if '_id' in doc and doc['_id'] is not None:
                    doc['_id'] = str(doc['_id'])
                # Convertir datetime a ISO string
                for key, value in list(doc.items()):
                    if isinstance(value, datetime):
                        doc[key] = value.isoformat()

            return results

        else:
            raise ValueError(f"Operación no soportada: {operation}")

    async def _generate_natural_response(
        self,
        question: str,
        query_plan: Dict,
        results: Any
    ) -> str:
        """Genera una respuesta en lenguaje natural basada en los resultados"""

        prompt = f"""Eres un asistente que presenta resultados de consultas de base de datos de forma clara y profesional.

PREGUNTA DEL USUARIO:
{question}

CONSULTA EJECUTADA:
{query_plan.get('explanation', 'Consulta a la base de datos')}

RESULTADOS:
{json.dumps(results, indent=2, ensure_ascii=False)[:2000]}

INSTRUCCIONES:
1. Responde la pregunta del usuario con los datos obtenidos
2. Presenta los resultados de forma clara y organizada
3. Si son muchos resultados, resume los más relevantes
4. Usa formato markdown para listas o tablas si es apropiado
5. Sé conciso pero informativo

RESPUESTA:"""

        try:
            response = self.llm_service.generate_response(prompt, temperature=0.3)
            return response
        except Exception as e:
            print(f"Error generando respuesta: {e}")
            return f"Resultados obtenidos: {json.dumps(results, indent=2, ensure_ascii=False)[:500]}"
