"""
Configuración de la aplicación usando pydantic-settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # MongoDB Configuration
    MONGODB_URI: str = Field(..., description="MongoDB Atlas connection URI")
    MONGODB_DB_NAME: str = Field(default="rag_database", description="Database name")

    # Groq API Configuration
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile", description="Groq model to use")

    # Application Configuration
    ENVIRONMENT: str = Field(default="development", description="Environment")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # Embedding Model Configuration
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence transformer model"
    )
    EMBEDDING_DIMENSION: int = Field(default=384, description="Embedding vector dimension")

    # Search Configuration
    MAX_SEARCH_RESULTS: int = Field(default=10, description="Maximum search results")
    SIMILARITY_THRESHOLD: float = Field(default=0.7, description="Similarity threshold")

    # Collection Names
    DOCUMENTS_COLLECTION: str = Field(default="documents", description="Documents collection")
    IMAGES_COLLECTION: str = Field(default="images", description="Images collection")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()
