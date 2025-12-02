"""
Funciones auxiliares y utilidades generales
"""
import hashlib
import json
from typing import Any, Dict, List
from datetime import datetime
import re


def generate_document_id(content: str) -> str:
    """
    Genera un ID único basado en el contenido

    Args:
        content: Contenido del documento

    Returns:
        Hash MD5 del contenido
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def clean_text(text: str) -> str:
    """
    Limpia texto eliminando caracteres especiales y espacios extra

    Args:
        text: Texto a limpiar

    Returns:
        Texto limpio
    """
    # Eliminar múltiples espacios
    text = re.sub(r'\s+', ' ', text)

    # Eliminar espacios al inicio y final
    text = text.strip()

    # Eliminar caracteres de control
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Divide texto en chunks con overlap

    Args:
        text: Texto a dividir
        chunk_size: Tamaño de cada chunk
        overlap: Overlap entre chunks

    Returns:
        Lista de chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

        if i + chunk_size >= len(words):
            break

    return chunks


def normalize_score(score: float, min_score: float = 0.0, max_score: float = 1.0) -> float:
    """
    Normaliza un score al rango [0, 1]

    Args:
        score: Score a normalizar
        min_score: Score mínimo
        max_score: Score máximo

    Returns:
        Score normalizado
    """
    if max_score == min_score:
        return 0.0

    normalized = (score - min_score) / (max_score - min_score)
    return max(0.0, min(1.0, normalized))


def format_timestamp(dt: datetime = None) -> str:
    """
    Formatea timestamp en formato ISO

    Args:
        dt: Datetime (usa now si no se proporciona)

    Returns:
        String con timestamp formateado
    """
    if dt is None:
        dt = datetime.utcnow()

    return dt.isoformat()


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Trunca texto a una longitud máxima

    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a agregar

    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Combina dos diccionarios recursivamente

    Args:
        dict1: Primer diccionario
        dict2: Segundo diccionario

    Returns:
        Diccionario combinado
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def validate_embedding_dimension(embedding: List[float], expected_dim: int) -> bool:
    """
    Valida que un embedding tenga la dimensión correcta

    Args:
        embedding: Vector de embedding
        expected_dim: Dimensión esperada

    Returns:
        True si la dimensión es correcta
    """
    return len(embedding) == expected_dim


def calculate_text_stats(text: str) -> Dict[str, Any]:
    """
    Calcula estadísticas de un texto

    Args:
        text: Texto a analizar

    Returns:
        Dict con estadísticas
    """
    words = text.split()
    sentences = text.split('.')

    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "avg_sentence_length": len(words) / len(sentences) if sentences else 0
    }


def batch_items(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Divide una lista en lotes

    Args:
        items: Lista de items
        batch_size: Tamaño de cada lote

    Returns:
        Lista de lotes
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extrae keywords simples de un texto (basado en frecuencia)

    Args:
        text: Texto del que extraer keywords
        top_n: Número de keywords a retornar

    Returns:
        Lista de keywords
    """
    # Lista de stopwords simple
    stopwords = {
        'el', 'la', 'de', 'en', 'y', 'a', 'los', 'las', 'del', 'un', 'una',
        'por', 'con', 'para', 'es', 'al', 'como', 'se', 'su', 'que', 'este',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'as', 'by', 'with', 'from', 'is', 'was', 'are', 'been'
    }

    # Limpiar y tokenizar
    words = re.findall(r'\b\w+\b', text.lower())

    # Filtrar stopwords y palabras cortas
    words = [w for w in words if w not in stopwords and len(w) > 3]

    # Contar frecuencias
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Ordenar por frecuencia
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Retornar top N
    return [word for word, _ in sorted_words[:top_n]]


def format_bytes(bytes_size: int) -> str:
    """
    Formatea tamaño en bytes a formato legible

    Args:
        bytes_size: Tamaño en bytes

    Returns:
        String formateado (ej: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0

    return f"{bytes_size:.2f} PB"
