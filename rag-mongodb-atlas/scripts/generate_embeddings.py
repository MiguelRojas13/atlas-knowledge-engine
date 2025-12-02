"""
Script para generar y actualizar embeddings en MongoDB
"""
import sys
import os
from pathlib import Path
import logging
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import mongodb
from config.settings import settings
from services.embedding_service import embedding_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_document_embeddings():
    """Genera embeddings para documentos"""
    try:
        mongodb.connect_sync()
        collection = mongodb.sync_db[settings.DOCUMENTS_COLLECTION]

        # Obtener documentos sin embeddings
        query = {"embedding": {"$exists": False}}
        total_docs = collection.count_documents(query)

        if total_docs == 0:
            logger.info("✅ Todos los documentos ya tienen embeddings")
            return

        logger.info(f"Generando embeddings para {total_docs} documentos...")

        # Procesar documentos en lotes
        batch_size = 32
        cursor = collection.find(query)

        processed = 0
        with tqdm(total=total_docs) as pbar:
            batch = []
            batch_ids = []

            for doc in cursor:
                # Combinar título y contenido
                text = f"{doc.get('title', '')} {doc.get('content', '')}"
                batch.append(text)
                batch_ids.append(doc['_id'])

                if len(batch) >= batch_size:
                    # Generar embeddings para el lote
                    embeddings = embedding_service.generate_text_embeddings_batch(batch)

                    # Actualizar documentos
                    for doc_id, embedding in zip(batch_ids, embeddings):
                        collection.update_one(
                            {"_id": doc_id},
                            {"$set": {"embedding": embedding}}
                        )

                    processed += len(batch)
                    pbar.update(len(batch))

                    # Limpiar lote
                    batch = []
                    batch_ids = []

            # Procesar lote restante
            if batch:
                embeddings = embedding_service.generate_text_embeddings_batch(batch)
                for doc_id, embedding in zip(batch_ids, embeddings):
                    collection.update_one(
                        {"_id": doc_id},
                        {"$set": {"embedding": embedding}}
                    )
                processed += len(batch)
                pbar.update(len(batch))

        logger.info(f"✅ {processed} embeddings de documentos generados")

    except Exception as e:
        logger.error(f"❌ Error generando embeddings de documentos: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def generate_image_embeddings():
    """Genera embeddings para imágenes"""
    try:
        mongodb.connect_sync()
        collection = mongodb.sync_db[settings.IMAGES_COLLECTION]

        # Obtener imágenes sin embeddings
        query = {"embedding": {"$exists": False}}
        total_images = collection.count_documents(query)

        if total_images == 0:
            logger.info("✅ Todas las imágenes ya tienen embeddings")
            return

        logger.info(f"Generando embeddings para {total_images} imágenes...")

        cursor = collection.find(query)
        processed = 0

        with tqdm(total=total_images) as pbar:
            for img_doc in cursor:
                try:
                    # Generar embedding (usando descripción como placeholder)
                    text = f"{img_doc.get('filename', '')} {img_doc.get('description', '')}"
                    embedding = embedding_service.generate_text_embedding(text)

                    # Actualizar documento
                    collection.update_one(
                        {"_id": img_doc['_id']},
                        {"$set": {"embedding": embedding}}
                    )

                    processed += 1
                    pbar.update(1)

                except Exception as e:
                    logger.error(f"Error procesando imagen {img_doc.get('filename')}: {e}")

        logger.info(f"✅ {processed} embeddings de imágenes generados")

    except Exception as e:
        logger.error(f"❌ Error generando embeddings de imágenes: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def verify_embeddings():
    """Verifica que todos los documentos tengan embeddings"""
    try:
        mongodb.connect_sync()

        # Verificar documentos
        docs_collection = mongodb.sync_db[settings.DOCUMENTS_COLLECTION]
        total_docs = docs_collection.count_documents({})
        docs_with_embeddings = docs_collection.count_documents(
            {"embedding": {"$exists": True}}
        )

        logger.info(f"\nDocumentos:")
        logger.info(f"  Total: {total_docs}")
        logger.info(f"  Con embeddings: {docs_with_embeddings}")
        logger.info(f"  Sin embeddings: {total_docs - docs_with_embeddings}")

        # Verificar imágenes
        images_collection = mongodb.sync_db[settings.IMAGES_COLLECTION]
        total_images = images_collection.count_documents({})
        images_with_embeddings = images_collection.count_documents(
            {"embedding": {"$exists": True}}
        )

        logger.info(f"\nImágenes:")
        logger.info(f"  Total: {total_images}")
        logger.info(f"  Con embeddings: {images_with_embeddings}")
        logger.info(f"  Sin embeddings: {total_images - images_with_embeddings}")

    except Exception as e:
        logger.error(f"Error verificando embeddings: {e}")
    finally:
        mongodb.disconnect_sync()


def main():
    """Función principal"""
    logger.info("=== Generando Embeddings ===")
    logger.info(f"Modelo: {settings.EMBEDDING_MODEL}")
    logger.info(f"Dimensión: {settings.EMBEDDING_DIMENSION}")

    # Generar embeddings de documentos
    logger.info("\n--- Procesando documentos ---")
    generate_document_embeddings()

    # Generar embeddings de imágenes
    logger.info("\n--- Procesando imágenes ---")
    generate_image_embeddings()

    # Verificar
    logger.info("\n--- Verificación ---")
    verify_embeddings()

    logger.info("\n✅ Proceso completado")
    logger.info("\nPróximos pasos:")
    logger.info("1. Asegúrate de crear los índices vectoriales en Atlas UI")
    logger.info("2. Ejecuta la aplicación: uvicorn main:app --reload")


if __name__ == "__main__":
    main()
