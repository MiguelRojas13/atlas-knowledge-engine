"""
Pydantic models para validación de datos
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SearchType(str, Enum):
    """Tipos de búsqueda disponibles"""
    VECTOR = "vector"
    HYBRID = "hybrid"
    FULLTEXT = "fulltext"


class DocumentBase(BaseModel):
    """Modelo base para documentos"""
    title: str = Field(..., description="Título del documento")
    content: str = Field(..., description="Contenido del documento")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadatos adicionales")


class DocumentCreate(DocumentBase):
    """Modelo para crear documentos"""
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags del documento")


class DocumentInDB(DocumentBase):
    """Modelo de documento en la base de datos"""
    id: str = Field(..., alias="_id", description="ID del documento")
    embedding: Optional[List[float]] = Field(default=None, description="Vector de embedding")
    tags: List[str] = Field(default_factory=list, description="Tags")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de actualización")

    class Config:
        populate_by_name = True


class ImageBase(BaseModel):
    """Modelo base para imágenes"""
    filename: str = Field(..., description="Nombre del archivo")
    description: Optional[str] = Field(None, description="Descripción de la imagen")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadatos adicionales")


class ImageCreate(ImageBase):
    """Modelo para crear imágenes"""
    image_path: str = Field(..., description="Ruta de la imagen")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")


class ImageInDB(ImageBase):
    """Modelo de imagen en la base de datos"""
    id: str = Field(..., alias="_id", description="ID de la imagen")
    image_path: str = Field(..., description="Ruta de la imagen")
    embedding: Optional[List[float]] = Field(default=None, description="Vector de embedding")
    tags: List[str] = Field(default_factory=list, description="Tags")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")

    class Config:
        populate_by_name = True


class SearchRequest(BaseModel):
    """Modelo para solicitudes de búsqueda"""
    query: str = Field(..., description="Texto de búsqueda", min_length=1)
    search_type: SearchType = Field(default=SearchType.VECTOR, description="Tipo de búsqueda")
    limit: int = Field(default=10, ge=1, le=100, description="Número máximo de resultados")
    collection: Optional[str] = Field(default="documents", description="Colección a buscar")


class SearchResult(BaseModel):
    """Modelo para resultados de búsqueda"""
    id: str = Field(..., description="ID del documento")
    score: float = Field(..., description="Score de similitud")
    title: Optional[str] = Field(None, description="Título")
    content: Optional[str] = Field(None, description="Contenido")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadatos")


class SearchResponse(BaseModel):
    """Modelo para respuesta de búsqueda"""
    results: List[SearchResult] = Field(..., description="Lista de resultados")
    total: int = Field(..., description="Total de resultados")
    query: str = Field(..., description="Query original")
    search_type: SearchType = Field(..., description="Tipo de búsqueda usado")


class RAGRequest(BaseModel):
    """Modelo para solicitudes RAG"""
    question: str = Field(..., description="Pregunta del usuario", min_length=1)
    context_limit: int = Field(default=5, ge=1, le=20, description="Número de contextos a recuperar")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperatura del modelo")
    max_tokens: int = Field(default=1024, ge=1, le=4096, description="Tokens máximos de respuesta")


class RAGResponse(BaseModel):
    """Modelo para respuesta RAG"""
    answer: str = Field(..., description="Respuesta generada")
    question: str = Field(..., description="Pregunta original")
    context: List[SearchResult] = Field(..., description="Contextos utilizados")
    model: str = Field(..., description="Modelo usado")


class HealthResponse(BaseModel):
    """Modelo para health check"""
    status: str = Field(..., description="Estado del servicio")
    database: str = Field(..., description="Estado de la base de datos")
