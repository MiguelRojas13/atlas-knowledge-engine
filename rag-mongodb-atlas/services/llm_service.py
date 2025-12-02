"""
Servicio de integración con Groq API para generación de texto
"""
from groq import Groq
from typing import List, Dict, Optional
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Servicio para interactuar con Groq API"""

    def __init__(self):
        """Inicializa el cliente de Groq"""
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente de Groq"""
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("✅ Cliente Groq inicializado")
        except Exception as e:
            logger.error(f"❌ Error inicializando Groq: {e}")
            raise

    def generate_response(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: Optional[str] = None
    ) -> str:
        """
        Genera una respuesta usando Groq

        Args:
            prompt: Prompt del usuario
            system_message: Mensaje de sistema (opcional)
            temperature: Temperatura del modelo (0-2)
            max_tokens: Máximo de tokens a generar
            model: Modelo a usar (usa el default si no se especifica)

        Returns:
            Respuesta generada por el modelo
        """
        try:
            messages = []

            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            model_to_use = model or settings.GROQ_MODEL

            response = self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            raise

    def generate_rag_response(
        self,
        question: str,
        context_documents: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Genera respuesta RAG usando contexto recuperado

        Args:
            question: Pregunta del usuario
            context_documents: Documentos de contexto
            temperature: Temperatura del modelo
            max_tokens: Tokens máximos

        Returns:
            Respuesta generada
        """
        try:
            # Construir contexto
            context_text = self._build_context(context_documents)

            # System message para RAG
            system_message = (
                "Eres un asistente útil que responde preguntas basándose "
                "en el contexto proporcionado. Si la respuesta no está en "
                "el contexto, indícalo claramente. No inventes información."
            )

            # Prompt con contexto
            prompt = f"""Contexto:
{context_text}

Pregunta: {question}

Respuesta basada en el contexto:"""

            return self.generate_response(
                prompt=prompt,
                system_message=system_message,
                temperature=temperature,
                max_tokens=max_tokens
            )

        except Exception as e:
            logger.error(f"Error generando respuesta RAG: {e}")
            raise

    def _build_context(self, documents: List[Dict]) -> str:
        """
        Construye el contexto a partir de documentos

        Args:
            documents: Lista de documentos

        Returns:
            Texto de contexto formateado
        """
        context_parts = []

        for i, doc in enumerate(documents, 1):
            title = doc.get("title", "Sin título")
            content = doc.get("content", "")

            context_parts.append(f"[Documento {i}] {title}\n{content}")

        return "\n\n".join(context_parts)

    def generate_summary(
        self,
        text: str,
        max_tokens: int = 256
    ) -> str:
        """
        Genera un resumen de un texto

        Args:
            text: Texto a resumir
            max_tokens: Tokens máximos del resumen

        Returns:
            Resumen generado
        """
        try:
            prompt = f"Resume el siguiente texto de forma concisa:\n\n{text}"

            return self.generate_response(
                prompt=prompt,
                temperature=0.5,
                max_tokens=max_tokens
            )

        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            raise


# Singleton instance
llm_service = LLMService()
