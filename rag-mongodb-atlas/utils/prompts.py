"""
Templates de prompts para RAG
"""


class PromptTemplates:
    """Templates de prompts para diferentes casos de uso"""

    # Prompt base para RAG
    RAG_SYSTEM_PROMPT = """Eres un asistente útil que responde preguntas basándose en el contexto proporcionado.

INSTRUCCIONES:
1. Responde SOLO basándote en la información del contexto
2. Si la respuesta no está en el contexto, dilo claramente
3. No inventes información
4. Sé conciso pero completo
5. Cita las fuentes cuando sea relevante
"""

    RAG_USER_PROMPT = """Contexto:
{context}

Pregunta: {question}

Respuesta:"""

    # Prompt para resumen
    SUMMARY_PROMPT = """Resume el siguiente texto de forma concisa y clara:

{text}

Resumen:"""

    # Prompt para extracción de información
    EXTRACTION_PROMPT = """Extrae la siguiente información del texto:

Información a extraer:
{fields}

Texto:
{text}

Información extraída (en formato JSON):"""

    # Prompt para clasificación
    CLASSIFICATION_PROMPT = """Clasifica el siguiente texto en una de estas categorías:

Categorías: {categories}

Texto: {text}

Clasificación:"""

    # Prompt conversacional
    CONVERSATIONAL_PROMPT = """Eres un asistente conversacional que ayuda a responder preguntas.

Historial de conversación:
{history}

Contexto relevante:
{context}

Pregunta actual: {question}

Respuesta:"""

    # Prompt para reformulación de queries
    QUERY_REFORMULATION_PROMPT = """Dado el historial de conversación y la pregunta actual, reformula la pregunta para que sea más clara y específica.

Historial:
{history}

Pregunta actual: {question}

Pregunta reformulada:"""

    @classmethod
    def format_rag_prompt(cls, context: str, question: str) -> dict:
        """
        Formatea el prompt RAG

        Args:
            context: Contexto de documentos
            question: Pregunta del usuario

        Returns:
            Dict con system y user prompts
        """
        return {
            "system": cls.RAG_SYSTEM_PROMPT,
            "user": cls.RAG_USER_PROMPT.format(
                context=context,
                question=question
            )
        }

    @classmethod
    def format_summary_prompt(cls, text: str) -> str:
        """Formatea prompt para resumen"""
        return cls.SUMMARY_PROMPT.format(text=text)

    @classmethod
    def format_extraction_prompt(cls, text: str, fields: list) -> str:
        """Formatea prompt para extracción"""
        fields_str = "\n".join([f"- {field}" for field in fields])
        return cls.EXTRACTION_PROMPT.format(
            text=text,
            fields=fields_str
        )

    @classmethod
    def format_classification_prompt(cls, text: str, categories: list) -> str:
        """Formatea prompt para clasificación"""
        categories_str = ", ".join(categories)
        return cls.CLASSIFICATION_PROMPT.format(
            text=text,
            categories=categories_str
        )

    @classmethod
    def format_conversational_prompt(
        cls,
        question: str,
        context: str,
        history: list
    ) -> str:
        """Formatea prompt conversacional"""
        history_str = "\n".join([
            f"Usuario: {h.get('question', '')}\nAsistente: {h.get('answer', '')}"
            for h in history
        ])

        return cls.CONVERSATIONAL_PROMPT.format(
            question=question,
            context=context,
            history=history_str
        )


# Configuración de prompts específicos por dominio
DOMAIN_PROMPTS = {
    "technical": {
        "system": "Eres un asistente técnico experto. Proporciona respuestas precisas y técnicas.",
        "style": "formal y técnico"
    },
    "casual": {
        "system": "Eres un asistente amigable y conversacional. Usa un lenguaje natural y cercano.",
        "style": "casual y amigable"
    },
    "educational": {
        "system": "Eres un tutor educativo. Explica conceptos de manera clara y pedagógica.",
        "style": "educativo y claro"
    },
    "creative": {
        "system": "Eres un asistente creativo. Proporciona respuestas imaginativas y originales.",
        "style": "creativo y original"
    }
}


def get_domain_prompt(domain: str = "technical") -> dict:
    """
    Obtiene un prompt específico para un dominio

    Args:
        domain: Dominio del prompt

    Returns:
        Dict con configuración del prompt
    """
    return DOMAIN_PROMPTS.get(domain, DOMAIN_PROMPTS["technical"])
