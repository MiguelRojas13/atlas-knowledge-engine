"""
Definición de colecciones y sus estructuras
"""
from typing import Dict, Any


class CollectionSchemas:
    """Esquemas de validación de MongoDB para las colecciones"""

    DOCUMENTS_SCHEMA = {
        "bsonType": "object",
        "required": ["title", "content", "created_at"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "Título del documento"
            },
            "content": {
                "bsonType": "string",
                "description": "Contenido del documento"
            },
            "embedding": {
                "bsonType": "array",
                "items": {
                    "bsonType": "double"
                },
                "description": "Vector de embedding del documento"
            },
            "tags": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "description": "Tags del documento"
            },
            "metadata": {
                "bsonType": "object",
                "description": "Metadatos adicionales"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Fecha de creación"
            },
            "updated_at": {
                "bsonType": "date",
                "description": "Fecha de última actualización"
            }
        }
    }

    IMAGES_SCHEMA = {
        "bsonType": "object",
        "required": ["filename", "image_path", "created_at"],
        "properties": {
            "filename": {
                "bsonType": "string",
                "description": "Nombre del archivo de imagen"
            },
            "image_path": {
                "bsonType": "string",
                "description": "Ruta al archivo de imagen"
            },
            "description": {
                "bsonType": "string",
                "description": "Descripción de la imagen"
            },
            "embedding": {
                "bsonType": "array",
                "items": {
                    "bsonType": "double"
                },
                "description": "Vector de embedding de la imagen"
            },
            "tags": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "description": "Tags de la imagen"
            },
            "metadata": {
                "bsonType": "object",
                "description": "Metadatos adicionales"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Fecha de creación"
            }
        }
    }

    @classmethod
    def get_validator(cls, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna un validador de MongoDB"""
        return {
            "$jsonSchema": schema
        }


class IndexDefinitions:
    """Definiciones de índices para las colecciones"""

    DOCUMENTS_INDEXES = [
        {
            "name": "title_text_index",
            "keys": [("title", "text"), ("content", "text")],
            "options": {
                "weights": {
                    "title": 10,
                    "content": 5
                }
            }
        },
        {
            "name": "tags_index",
            "keys": [("tags", 1)],
            "options": {}
        },
        {
            "name": "created_at_index",
            "keys": [("created_at", -1)],
            "options": {}
        }
    ]

    IMAGES_INDEXES = [
        {
            "name": "filename_index",
            "keys": [("filename", 1)],
            "options": {"unique": True}
        },
        {
            "name": "tags_index",
            "keys": [("tags", 1)],
            "options": {}
        },
        {
            "name": "created_at_index",
            "keys": [("created_at", -1)],
            "options": {}
        }
    ]

    # Definición de índices vectoriales (Atlas Search)
    VECTOR_SEARCH_INDEX = {
        "name": "vector_index",
        "type": "vectorSearch",
        "definition": {
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 384,  # Debe coincidir con EMBEDDING_DIMENSION
                    "similarity": "cosine"
                }
            ]
        }
    }
