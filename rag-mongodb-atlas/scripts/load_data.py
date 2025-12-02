"""
Script para cargar datos desde archivos a MongoDB
"""
import sys
import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import mongodb
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_json_documents(file_path: Path) -> List[Dict[str, Any]]:
    """Carga documentos desde archivo JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Si es un solo documento, convertirlo en lista
            if isinstance(data, dict):
                data = [data]

            return data
    except Exception as e:
        logger.error(f"Error cargando JSON {file_path}: {e}")
        return []


def load_csv_documents(file_path: Path) -> List[Dict[str, Any]]:
    """Carga documentos desde archivo CSV"""
    try:
        documents = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                documents.append(row)
        return documents
    except Exception as e:
        logger.error(f"Error cargando CSV {file_path}: {e}")
        return []


def load_txt_document(file_path: Path) -> Dict[str, Any]:
    """Carga un documento desde archivo TXT"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "title": file_path.stem,
            "content": content,
            "metadata": {
                "source_file": str(file_path),
                "file_type": "txt"
            }
        }
    except Exception as e:
        logger.error(f"Error cargando TXT {file_path}: {e}")
        return None


def prepare_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Prepara un documento para inserción"""
    prepared = {
        "title": doc.get("title", "Sin título"),
        "content": doc.get("content", ""),
        "tags": doc.get("tags", []),
        "metadata": doc.get("metadata", {}),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    return prepared


def load_documents_to_db():
    """Carga documentos a MongoDB"""
    try:
        mongodb.connect_sync()
        collection = mongodb.sync_db[settings.DOCUMENTS_COLLECTION]

        # Directorio de documentos
        docs_dir = Path(__file__).parent.parent / "data" / "raw" / "documents"

        if not docs_dir.exists():
            logger.warning(f"Directorio no existe: {docs_dir}")
            return

        all_documents = []

        # Procesar archivos JSON
        for json_file in docs_dir.glob("*.json"):
            logger.info(f"Cargando: {json_file.name}")
            docs = load_json_documents(json_file)
            all_documents.extend(docs)

        # Procesar archivos CSV
        for csv_file in docs_dir.glob("*.csv"):
            logger.info(f"Cargando: {csv_file.name}")
            docs = load_csv_documents(csv_file)
            all_documents.extend(docs)

        # Procesar archivos TXT
        for txt_file in docs_dir.glob("*.txt"):
            logger.info(f"Cargando: {txt_file.name}")
            doc = load_txt_document(txt_file)
            if doc:
                all_documents.append(doc)

        if not all_documents:
            logger.warning("No se encontraron documentos para cargar")
            logger.info("\nColoca tus archivos en: data/raw/documents/")
            logger.info("Formatos soportados: JSON, CSV, TXT")
            return

        # Preparar documentos
        prepared_docs = [prepare_document(doc) for doc in all_documents]

        # Insertar en MongoDB
        if prepared_docs:
            result = collection.insert_many(prepared_docs)
            logger.info(f"✅ {len(result.inserted_ids)} documentos insertados")

            # Mostrar estadísticas
            total = collection.count_documents({})
            logger.info(f"Total de documentos en la colección: {total}")

    except Exception as e:
        logger.error(f"❌ Error cargando documentos: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def load_images_to_db():
    """Carga metadatos de imágenes a MongoDB"""
    try:
        mongodb.connect_sync()
        collection = mongodb.sync_db[settings.IMAGES_COLLECTION]

        images_dir = Path(__file__).parent.parent / "data" / "raw" / "images"

        if not images_dir.exists():
            logger.warning(f"Directorio no existe: {images_dir}")
            return

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        image_files = [f for f in images_dir.iterdir()
                      if f.suffix.lower() in image_extensions]

        if not image_files:
            logger.warning("No se encontraron imágenes")
            logger.info("\nColoca tus imágenes en: data/raw/images/")
            return

        image_documents = []

        for img_file in image_files:
            doc = {
                "filename": img_file.name,
                "image_path": str(img_file),
                "description": f"Imagen: {img_file.stem}",
                "tags": [],
                "metadata": {
                    "file_size": img_file.stat().st_size,
                    "extension": img_file.suffix
                },
                "created_at": datetime.utcnow()
            }
            image_documents.append(doc)

        if image_documents:
            result = collection.insert_many(image_documents)
            logger.info(f"✅ {len(result.inserted_ids)} imágenes insertadas")

            total = collection.count_documents({})
            logger.info(f"Total de imágenes en la colección: {total}")

    except Exception as e:
        logger.error(f"❌ Error cargando imágenes: {e}")
        raise
    finally:
        mongodb.disconnect_sync()


def main():
    """Función principal"""
    logger.info("=== Cargando datos a MongoDB ===")

    # Cargar documentos
    logger.info("\n--- Cargando documentos ---")
    load_documents_to_db()

    # Cargar imágenes
    logger.info("\n--- Cargando imágenes ---")
    load_images_to_db()

    logger.info("\n✅ Carga de datos completada")
    logger.info("\nPróximo paso:")
    logger.info("python scripts/generate_embeddings.py")


if __name__ == "__main__":
    main()
