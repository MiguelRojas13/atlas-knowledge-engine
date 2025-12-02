"""
Rutas y endpoints de la API
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from models.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
    RAGRequest,
    RAGResponse
)
from services.search_service import search_service
from services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["API"])


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Endpoint para búsqueda de documentos

    Soporta búsqueda vectorial, full-text e híbrida
    """
    try:
        logger.info(f"Search request: {request.query} ({request.search_type})")

        # Realizar búsqueda
        results = await search_service.search(
            query=request.query,
            search_type=request.search_type,
            collection_name=request.collection,
            limit=request.limit
        )

        # Formatear resultados
        search_results = [
            SearchResult(
                id=str(doc.get("_id", "")),
                score=doc.get("score", 0.0),
                title=doc.get("title"),
                content=doc.get("content"),
                metadata=doc.get("metadata", {})
            )
            for doc in results
        ]

        response = SearchResponse(
            results=search_results,
            total=len(search_results),
            query=request.query,
            search_type=request.search_type
        )

        return response

    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en búsqueda: {str(e)}"
        )


@router.post("/rag", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """
    Endpoint para consultas RAG

    Recupera contexto relevante y genera respuesta usando LLM
    """
    try:
        logger.info(f"RAG request: {request.question}")

        # Generar respuesta RAG
        result = await rag_service.generate_answer(
            question=request.question,
            context_limit=request.context_limit,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        # Formatear contexto
        context_results = [
            SearchResult(
                id=ctx.get("id", ""),
                score=ctx.get("score", 0.0),
                title=ctx.get("title"),
                content=ctx.get("content"),
                metadata=ctx.get("metadata", {})
            )
            for ctx in result.get("context", [])
        ]

        response = RAGResponse(
            answer=result["answer"],
            question=result["question"],
            context=context_results,
            model=result["model"]
        )

        return response

    except Exception as e:
        logger.error(f"Error in RAG endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en RAG: {str(e)}"
        )


@router.get("/collections")
async def list_collections():
    """
    Lista las colecciones disponibles en la base de datos
    """
    try:
        from config.database import mongodb

        # Obtener lista de colecciones
        collections = await mongodb.db.list_collection_names()

        return {
            "collections": collections,
            "total": len(collections)
        }

    except Exception as e:
        logger.error(f"Error listing collections: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listando colecciones: {str(e)}"
        )


@router.get("/collections/{collection_name}/stats")
async def collection_stats(collection_name: str):
    """
    Obtiene estadísticas de una colección
    """
    try:
        from config.database import mongodb

        collection = mongodb.get_collection(collection_name)

        # Contar documentos
        count = await collection.count_documents({})

        # Obtener un documento de ejemplo
        sample = await collection.find_one({})

        return {
            "collection": collection_name,
            "document_count": count,
            "sample_document": sample
        }

    except Exception as e:
        logger.error(f"Error getting collection stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )
