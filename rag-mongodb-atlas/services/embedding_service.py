"""
Servicio de generación de embeddings para texto e imágenes
"""
from sentence_transformers import SentenceTransformer
from PIL import Image
import numpy as np
from typing import List, Union
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Servicio para generar embeddings de texto e imágenes"""

    def __init__(self):
        """Inicializa el modelo de embeddings"""
        self.model = None
        self._load_model()

    def _load_model(self):
        """Carga el modelo de sentence transformers"""
        try:
            logger.info(f"Cargando modelo: {settings.EMBEDDING_MODEL}")
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("✅ Modelo de embeddings cargado")
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {e}")
            raise

    def generate_text_embedding(self, text: str) -> List[float]:
        """
        Genera embedding para un texto

        Args:
            text: Texto a convertir en embedding

        Returns:
            Vector de embedding como lista de floats
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generando embedding de texto: {e}")
            raise

    def generate_text_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings para múltiples textos (batch)

        Args:
            texts: Lista de textos

        Returns:
            Lista de vectores de embedding
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generando embeddings batch: {e}")
            raise

    def generate_image_embedding(self, image_path: str) -> List[float]:
        """
        Genera embedding para una imagen

        Args:
            image_path: Ruta a la imagen

        Returns:
            Vector de embedding como lista de floats
        """
        try:
            # Cargar imagen
            image = Image.open(image_path)

            # Para modelos que soportan imágenes (CLIP-like)
            # Si el modelo actual no soporta imágenes, necesitarías usar un modelo diferente
            # Por ahora, generamos un embedding basado en el nombre de archivo como placeholder
            logger.warning("Usando embedding de texto como placeholder para imágenes")
            text_representation = f"imagen: {image_path}"
            return self.generate_text_embedding(text_representation)

        except Exception as e:
            logger.error(f"Error generando embedding de imagen: {e}")
            raise

    def generate_combined_embedding(
        self,
        text: str,
        image_path: str = None,
        text_weight: float = 0.7
    ) -> List[float]:
        """
        Genera embedding combinado de texto e imagen

        Args:
            text: Texto a codificar
            image_path: Ruta a la imagen (opcional)
            text_weight: Peso del texto en la combinación (0-1)

        Returns:
            Vector de embedding combinado
        """
        try:
            text_emb = self.generate_text_embedding(text)

            if image_path:
                image_emb = self.generate_image_embedding(image_path)

                # Combinar embeddings con pesos
                text_emb_array = np.array(text_emb)
                image_emb_array = np.array(image_emb)

                combined = (text_weight * text_emb_array +
                           (1 - text_weight) * image_emb_array)

                return combined.tolist()
            else:
                return text_emb

        except Exception as e:
            logger.error(f"Error generando embedding combinado: {e}")
            raise

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula similitud coseno entre dos vectores

        Args:
            vec1: Primer vector
            vec2: Segundo vector

        Returns:
            Similitud coseno (0-1)
        """
        try:
            v1 = np.array(vec1)
            v2 = np.array(vec2)

            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)

            similarity = dot_product / (norm_v1 * norm_v2)
            return float(similarity)

        except Exception as e:
            logger.error(f"Error calculando similitud: {e}")
            raise


# Singleton instance
embedding_service = EmbeddingService()
