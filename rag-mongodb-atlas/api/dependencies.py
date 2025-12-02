"""
Dependencias compartidas de FastAPI
"""
from fastapi import Header, HTTPException, status
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Verifica API key (opcional, para proteger endpoints)

    Args:
        x_api_key: API key del header

    Raises:
        HTTPException: Si la API key es inválida
    """
    # Por ahora, esto es opcional y deshabilitado
    # Puedes agregar validación de API key aquí si lo necesitas
    pass


async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Obtiene el usuario actual desde el token de autorización

    Args:
        authorization: Token de autorización

    Returns:
        Usuario actual (placeholder)
    """
    # Placeholder para autenticación
    # Implementa tu lógica de autenticación aquí si la necesitas
    return {"user_id": "anonymous"}


def log_request(endpoint: str):
    """
    Decorator para logging de requests

    Args:
        endpoint: Nombre del endpoint
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger.info(f"Request to {endpoint}")
            result = await func(*args, **kwargs)
            logger.info(f"Response from {endpoint}")
            return result
        return wrapper
    return decorator
