"""
Servicio RAG (Retrieval-Augmented Generation) completo
"""
from typing import List, Dict, Any
import logging

from services.search_service import search_service
from services.llm_service import llm_service
from models.schemas import SearchType

logger = logging.getLogger(__name__)


class RAGService:
    """Servicio para pipeline RAG completo"""

    async def generate_answer(
        self,
        question: str,
        context_limit: int = 5,
        search_type: SearchType = SearchType.HYBRID,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        collection_name: str = None
    ) -> Dict[str, Any]:
        """
        Genera una respuesta usando RAG

        Args:
            question: Pregunta del usuario
            context_limit: Número de documentos de contexto
            search_type: Tipo de búsqueda para recuperar contexto
            temperature: Temperatura del modelo
            max_tokens: Tokens máximos de respuesta
            collection_name: Colección a buscar

        Returns:
            Dict con respuesta, pregunta y contexto usado
        """
        try:
            logger.info(f"RAG Query: '{question}'")

            # 1. Recuperar documentos relevantes
            context_docs = await search_service.search(
                query=question,
                search_type=search_type,
                collection_name=collection_name,
                limit=context_limit
            )

            if not context_docs:
                return {
                    "answer": "No se encontraron documentos relevantes para responder la pregunta.",
                    "question": question,
                    "context": [],
                    "model": "N/A"
                }

            # 2. Preparar contexto para el LLM
            context_for_llm = [
                {
                    "title": doc.get("title", "Sin título"),
                    "content": doc.get("content", ""),
                    "score": doc.get("score", 0)
                }
                for doc in context_docs
            ]

            # 3. Generar respuesta usando LLM
            answer = llm_service.generate_rag_response(
                question=question,
                context_documents=context_for_llm,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # 4. Preparar respuesta completa
            result = {
                "answer": answer,
                "question": question,
                "context": [
                    {
                        "id": str(doc.get("_id", "")),
                        "title": doc.get("title", ""),
                        "content": doc.get("content", "")[:500] + "...",  # Truncar para respuesta
                        "score": doc.get("score", 0),
                        "metadata": doc.get("metadata", {})
                    }
                    for doc in context_docs
                ],
                "model": "groq"
            }

            logger.info(f"RAG Answer generado con {len(context_docs)} contextos")
            return result

        except Exception as e:
            logger.error(f"Error en RAG pipeline: {e}")
            raise

    async def multi_query_rag(
        self,
        questions: List[str],
        context_limit: int = 5,
        temperature: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Procesa múltiples preguntas con RAG

        Args:
            questions: Lista de preguntas
            context_limit: Documentos de contexto por pregunta
            temperature: Temperatura del modelo

        Returns:
            Lista de respuestas RAG
        """
        try:
            results = []

            for question in questions:
                result = await self.generate_answer(
                    question=question,
                    context_limit=context_limit,
                    temperature=temperature
                )
                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Error en multi-query RAG: {e}")
            raise

    async def conversational_rag(
        self,
        question: str,
        conversation_history: List[Dict[str, str]],
        context_limit: int = 5,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        RAG conversacional que considera el historial

        Args:
            question: Pregunta actual
            conversation_history: Historial de conversación
            context_limit: Documentos de contexto
            temperature: Temperatura del modelo

        Returns:
            Respuesta RAG con contexto conversacional
        """
        try:
            # Reformular pregunta considerando el historial
            reformulated_query = self._reformulate_with_history(
                question,
                conversation_history
            )

            # Generar respuesta con query reformulada
            result = await self.generate_answer(
                question=reformulated_query,
                context_limit=context_limit,
                temperature=temperature
            )

            # Mantener la pregunta original en la respuesta
            result["original_question"] = question
            result["reformulated_query"] = reformulated_query

            return result

        except Exception as e:
            logger.error(f"Error en conversational RAG: {e}")
            raise

    def _reformulate_with_history(
        self,
        question: str,
        history: List[Dict[str, str]]
    ) -> str:
        """
        Reformula la pregunta considerando el historial

        Args:
            question: Pregunta actual
            history: Historial de conversación

        Returns:
            Pregunta reformulada
        """
        if not history:
            return question

        # Tomar las últimas 3 interacciones
        recent_history = history[-3:]

        # Construir contexto de historial
        history_context = "\n".join([
            f"Usuario: {h.get('question', '')}\nAsistente: {h.get('answer', '')}"
            for h in recent_history
        ])

        # Reformular considerando el contexto
        reformulated = f"""Historial de conversación:
{history_context}

Pregunta actual: {question}

Pregunta reformulada considerando el contexto:"""

        # Nota: En una implementación completa, usarías el LLM para reformular
        # Por ahora, retornamos la pregunta original con algo de contexto
        return f"{question} (contexto: {history[-1].get('question', '') if history else ''})"


# Singleton instance
rag_service = RAGService()
