"""
Script para crear índices en MongoDB Atlas
Incluye índices de texto, regulares y configuración para índices vectoriales
"""
import sys
import os
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import mongodb
from config.settings import settings
from models.collections import IndexDefinitions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_text_indexes():
    """Crea índices de texto y regulares"""
    try:
        mongodb.connect_sync()
        db = mongodb.sync_db

        # Índices para documentos
        logger.info(f"Creando índices para {settings.DOCUMENTS_COLLECTION}")
        docs_collection = db[settings.DOCUMENTS_COLLECTION]

        for index_def in IndexDefinitions.DOCUMENTS_INDEXES:
            try:
                docs_collection.create_index(
                    index_def["keys"],
                    name=index_def["name"],
                    **index_def["options"]
                )
                logger.info(f"✅ Índice creado: {index_def['name']}")
            except Exception as e:
                logger.warning(f"⚠️  Índice {index_def['name']} ya existe o error: {e}")

        # Índices para imágenes
        logger.info(f"Creando índices para {settings.IMAGES_COLLECTION}")
        images_collection = db[settings.IMAGES_COLLECTION]

        for index_def in IndexDefinitions.IMAGES_INDEXES:
            try:
                images_collection.create_index(
                    index_def["keys"],
                    name=index_def["name"],
                    **index_def["options"]
                )
                logger.info(f"✅ Índice creado: {index_def['name']}")
            except Exception as e:
                logger.warning(f"⚠️  Índice {index_def['name']} ya existe o error: {e}")

        logger.info("✅ Índices de texto creados")

    except Exception as e:
        logger.error(f"❌ Error creando índices: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def print_vector_index_instructions():
    """Imprime instrucciones para crear índices vectoriales en Atlas"""
    logger.info("\n" + "="*70)
    logger.info("CREACIÓN DE ÍNDICES VECTORIALES EN MONGODB ATLAS")
    logger.info("="*70)
    logger.info("\nLos índices vectoriales deben crearse desde la UI de MongoDB Atlas:")
    logger.info("\n1. Ve a tu cluster en MongoDB Atlas")
    logger.info("2. Haz clic en 'Search' en el menú lateral")
    logger.info("3. Clic en 'Create Search Index'")
    logger.info("4. Selecciona 'JSON Editor'")
    logger.info("5. Pega la siguiente configuración:\n")

    # Configuración para documentos
    vector_config = {
        "mappings": {
            "dynamic": True,
            "fields": {
                "embedding": {
                    "type": "knnVector",
                    "dimensions": settings.EMBEDDING_DIMENSION,
                    "similarity": "cosine"
                }
            }
        }
    }

    import json
    logger.info("CONFIGURACIÓN PARA COLECCIÓN DE DOCUMENTOS:")
    logger.info(f"Nombre del índice: vector_index")
    logger.info(f"Colección: {settings.DOCUMENTS_COLLECTION}")
    logger.info(json.dumps(vector_config, indent=2))

    logger.info("\n" + "-"*70)
    logger.info("CONFIGURACIÓN PARA COLECCIÓN DE IMÁGENES:")
    logger.info(f"Nombre del índice: vector_index")
    logger.info(f"Colección: {settings.IMAGES_COLLECTION}")
    logger.info(json.dumps(vector_config, indent=2))

    logger.info("\n" + "="*70)
    logger.info("Después de crear los índices vectoriales en Atlas UI,")
    logger.info("puedes continuar con la carga de datos.")
    logger.info("="*70 + "\n")


def main():
    """Función principal"""
    logger.info("=== Creando índices ===")

    # Crear índices de texto y regulares
    create_text_indexes()

    # Imprimir instrucciones para índices vectoriales
    print_vector_index_instructions()

    logger.info("\n✅ Proceso completado")


if __name__ == "__main__":
    main()
