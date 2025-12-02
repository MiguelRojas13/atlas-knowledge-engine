"""
Conexión y gestión de MongoDB Atlas
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """Gestión de conexión a MongoDB Atlas"""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.sync_client: Optional[MongoClient] = None
        self.sync_db = None

    async def connect(self):
        """Establecer conexión asíncrona a MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.db = self.client[settings.MONGODB_DB_NAME]

            # Verificar conexión
            await self.client.admin.command('ping')
            logger.info(f"✅ Conectado a MongoDB: {settings.MONGODB_DB_NAME}")

        except Exception as e:
            logger.error(f"❌ Error conectando a MongoDB: {e}")
            raise

    async def disconnect(self):
        """Cerrar conexión asíncrona"""
        if self.client:
            self.client.close()
            logger.info("🔌 Desconectado de MongoDB")

    def connect_sync(self):
        """Establecer conexión síncrona (para scripts)"""
        try:
            self.sync_client = MongoClient(settings.MONGODB_URI)
            self.sync_db = self.sync_client[settings.MONGODB_DB_NAME]

            # Verificar conexión
            self.sync_client.admin.command('ping')
            logger.info(f"✅ Conexión síncrona a MongoDB: {settings.MONGODB_DB_NAME}")

        except Exception as e:
            logger.error(f"❌ Error en conexión síncrona: {e}")
            raise

    def disconnect_sync(self):
        """Cerrar conexión síncrona"""
        if self.sync_client:
            self.sync_client.close()
            logger.info("🔌 Desconectado de MongoDB (sync)")

    def get_collection(self, collection_name: str):
        """Obtener colección asíncrona"""
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db[collection_name]

    def get_collection_sync(self, collection_name: str):
        """Obtener colección síncrona"""
        if not self.sync_db:
            raise RuntimeError("Sync database not connected. Call connect_sync() first.")
        return self.sync_db[collection_name]


# Singleton instance
mongodb = MongoDB()
