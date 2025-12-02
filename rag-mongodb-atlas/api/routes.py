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
from services.query_service import QueryService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["API"])
query_service = QueryService()


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

        # Convertir ObjectId a string
        if sample and '_id' in sample:
            sample['_id'] = str(sample['_id'])

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


@router.get("/database/schema")
async def get_database_schema():
    """
    Obtiene la estructura dinámica de la base de datos conectada
    """
    try:
        from config.database import mongodb
        from config.settings import settings

        db = mongodb.db

        # Obtener todas las colecciones
        collections_info = []

        for coll_name in await db.list_collection_names():
            collection = mongodb.get_collection(coll_name)
            count = await collection.count_documents({})

            # Obtener un documento de muestra para ver campos
            sample = await collection.find_one({})
            fields = []

            if sample:
                for key, value in sample.items():
                    if key != '_id':
                        field_type = type(value).__name__
                        fields.append({
                            "name": key,
                            "type": field_type
                        })

            collections_info.append({
                "name": coll_name,
                "count": count,
                "fields": fields[:10]  # Limitar a 10 campos
            })

        return {
            "database": settings.MONGODB_DB_NAME,
            "collections": collections_info,
            "total_collections": len(collections_info)
        }

    except Exception as e:
        logger.error(f"Error getting database schema: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo esquema: {str(e)}"
        )


@router.post("/query")
async def natural_language_query(request: dict):
    """
    Endpoint para consultas en lenguaje natural

    Traduce preguntas en lenguaje natural a consultas MongoDB y ejecuta
    """
    try:
        question = request.get("question")
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La pregunta es requerida"
            )

        logger.info(f"Natural language query: {question}")

        # Procesar consulta
        result = await query_service.natural_language_query(question)

        return result

    except Exception as e:
        logger.error(f"Error in natural language query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en consulta: {str(e)}"
        )
