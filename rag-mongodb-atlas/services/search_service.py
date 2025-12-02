"""
Servicio de búsqueda vectorial e híbrida usando MongoDB Atlas
"""
from typing import List, Dict, Any, Optional
import logging

from config.database import mongodb
from config.settings import settings
from services.embedding_service import embedding_service
from models.schemas import SearchType

logger = logging.getLogger(__name__)


class SearchService:
    """Servicio para búsqueda vectorial e híbrida en MongoDB Atlas"""

    async def vector_search(
        self,
        query: str,
        collection_name: str = None,
        limit: int = 10,
        min_score: float = None
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda vectorial usando Atlas Vector Search

        Args:
            query: Query de búsqueda
            collection_name: Nombre de la colección
            limit: Número máximo de resultados
            min_score: Score mínimo de similitud

        Returns:
            Lista de documentos con scores
        """
        try:
            # Generar embedding del query
            query_embedding = embedding_service.generate_text_embedding(query)

            # Obtener colección
            coll_name = collection_name or settings.DOCUMENTS_COLLECTION
            collection = mongodb.get_collection(coll_name)

            # Pipeline de agregación para vector search
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": limit * 10,
                        "limit": limit
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "content": 1,
                        "metadata": 1,
                        "tags": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]

            # Agregar filtro de score mínimo si se especifica
            if min_score:
                pipeline.append({
                    "$match": {
                        "score": {"$gte": min_score}
                    }
                })

            # Ejecutar búsqueda
            cursor = collection.aggregate(pipeline)
            results = await cursor.to_list(length=limit)

            logger.info(f"Vector search: {len(results)} resultados para '{query}'")
            return results

        except Exception as e:
            logger.error(f"Error en vector search: {e}")
            raise

    async def fulltext_search(
        self,
        query: str,
        collection_name: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda de texto completo usando índices de texto de MongoDB

        Args:
            query: Query de búsqueda
            collection_name: Nombre de la colección
            limit: Número máximo de resultados

        Returns:
            Lista de documentos con scores
        """
        try:
            # Obtener colección
            coll_name = collection_name or settings.DOCUMENTS_COLLECTION
            collection = mongodb.get_collection(coll_name)

            # Búsqueda de texto
            cursor = collection.find(
                {"$text": {"$search": query}},
                {"score": {"$meta": "textScore"}}
            ).sort(
                [("score", {"$meta": "textScore"})]
            ).limit(limit)

            results = await cursor.to_list(length=limit)

            logger.info(f"Fulltext search: {len(results)} resultados para '{query}'")
            return results

        except Exception as e:
            logger.error(f"Error en fulltext search: {e}")
            raise

    async def hybrid_search(
        self,
        query: str,
        collection_name: str = None,
        limit: int = 10,
        vector_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda híbrida combinando vector search y fulltext search

        Args:
            query: Query de búsqueda
            collection_name: Nombre de la colección
            limit: Número máximo de resultados
            vector_weight: Peso de la búsqueda vectorial (0-1)

        Returns:
            Lista de documentos con scores combinados
        """
        try:
            # Realizar ambas búsquedas en paralelo
            vector_results = await self.vector_search(query, collection_name, limit * 2)
            text_results = await self.fulltext_search(query, collection_name, limit * 2)

            # Combinar resultados
            combined_results = self._combine_search_results(
                vector_results,
                text_results,
                vector_weight
            )

            # Limitar resultados
            final_results = combined_results[:limit]

            logger.info(f"Hybrid search: {len(final_results)} resultados para '{query}'")
            return final_results

        except Exception as e:
            logger.error(f"Error en hybrid search: {e}")
            raise

    def _combine_search_results(
        self,
        vector_results: List[Dict],
        text_results: List[Dict],
        vector_weight: float
    ) -> List[Dict[str, Any]]:
        """
        Combina resultados de búsqueda vectorial y de texto

        Args:
            vector_results: Resultados de vector search
            text_results: Resultados de fulltext search
            vector_weight: Peso de vector search (0-1)

        Returns:
            Lista combinada y ordenada de resultados
        """
        # Diccionario para almacenar scores combinados
        combined = {}

        # Normalizar y combinar scores de vector search
        max_vector_score = max([r.get("score", 0) for r in vector_results], default=1)
        for result in vector_results:
            doc_id = str(result["_id"])
            normalized_score = result.get("score", 0) / max_vector_score
            combined[doc_id] = {
                "document": result,
                "score": normalized_score * vector_weight
            }

        # Normalizar y combinar scores de text search
        max_text_score = max([r.get("score", 0) for r in text_results], default=1)
        text_weight = 1 - vector_weight

        for result in text_results:
            doc_id = str(result["_id"])
            normalized_score = result.get("score", 0) / max_text_score

            if doc_id in combined:
                combined[doc_id]["score"] += normalized_score * text_weight
            else:
                combined[doc_id] = {
                    "document": result,
                    "score": normalized_score * text_weight
                }

        # Ordenar por score combinado
        sorted_results = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        # Retornar documentos con score combinado
        return [
            {**item["document"], "score": item["score"]}
            for item in sorted_results
        ]

    async def search(
        self,
        query: str,
        search_type: SearchType = SearchType.VECTOR,
        collection_name: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Método unificado de búsqueda

        Args:
            query: Query de búsqueda
            search_type: Tipo de búsqueda
            collection_name: Nombre de la colección
            limit: Número máximo de resultados

        Returns:
            Lista de resultados
        """
        if search_type == SearchType.VECTOR:
            return await self.vector_search(query, collection_name, limit)
        elif search_type == SearchType.FULLTEXT:
            return await self.fulltext_search(query, collection_name, limit)
        elif search_type == SearchType.HYBRID:
            return await self.hybrid_search(query, collection_name, limit)
        else:
            raise ValueError(f"Tipo de búsqueda no soportado: {search_type}")


# Singleton instance
search_service = SearchService()
