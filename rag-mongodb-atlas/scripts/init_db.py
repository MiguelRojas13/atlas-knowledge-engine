"""
Script para inicializar la base de datos MongoDB
Crea colecciones e índices necesarios
"""
import sys
import os
import logging
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import mongodb
from config.settings import settings
from models.collections import CollectionSchemas, IndexDefinitions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_collections():
    """Crea las colecciones con validación de esquema"""
    try:
        # Conectar a MongoDB (sync)
        mongodb.connect_sync()

        db = mongodb.sync_db

        # Crear colección de documentos
        logger.info(f"Creando colección: {settings.DOCUMENTS_COLLECTION}")
        if settings.DOCUMENTS_COLLECTION not in db.list_collection_names():
            db.create_collection(
                settings.DOCUMENTS_COLLECTION,
                validator=CollectionSchemas.get_validator(CollectionSchemas.DOCUMENTS_SCHEMA)
            )
            logger.info(f"✅ Colección {settings.DOCUMENTS_COLLECTION} creada")
        else:
            logger.info(f"⚠️  Colección {settings.DOCUMENTS_COLLECTION} ya existe")

        # Crear colección de imágenes
        logger.info(f"Creando colección: {settings.IMAGES_COLLECTION}")
        if settings.IMAGES_COLLECTION not in db.list_collection_names():
            db.create_collection(
                settings.IMAGES_COLLECTION,
                validator=CollectionSchemas.get_validator(CollectionSchemas.IMAGES_SCHEMA)
            )
            logger.info(f"✅ Colección {settings.IMAGES_COLLECTION} creada")
        else:
            logger.info(f"⚠️  Colección {settings.IMAGES_COLLECTION} ya existe")

        logger.info("✅ Colecciones creadas exitosamente")

    except Exception as e:
        logger.error(f"❌ Error creando colecciones: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def main():
    """Función principal"""
    logger.info("=== Iniciando creación de base de datos ===")
    logger.info(f"Base de datos: {settings.MONGODB_DB_NAME}")

    create_collections()

    logger.info("=== Base de datos inicializada ===")
    logger.info("\nPróximos pasos:")
    logger.info("1. Crear índices: python scripts/create_indexes.py")
    logger.info("2. Cargar datos: python scripts/load_data.py")
    logger.info("3. Generar embeddings: python scripts/generate_embeddings.py")


if __name__ == "__main__":
    main()
