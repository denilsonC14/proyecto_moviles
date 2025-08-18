from abc import ABC, abstractmethod
from typing import List, Union


class EmbeddingService(ABC):
    """Interface para servicios de generación de embeddings."""
    
    @abstractmethod
    async def generar_embedding(self, texto: str) -> List[float]:
        """
        Genera un embedding vectorial para un texto.
        
        Args:
            texto: El texto para el cual generar el embedding
            
        Returns:
            List[float]: Vector de embedding del texto
        """
        pass
    
    @abstractmethod
    async def generar_embeddings_batch(
        self, 
        textos: List[str]
    ) -> List[List[float]]:
        """
        Genera embeddings para múltiples textos de forma eficiente.
        
        Args:
            textos: Lista de textos para generar embeddings
            
        Returns:
            List[List[float]]: Lista de vectores de embedding
        """
        pass
    
    @abstractmethod
    def obtener_dimension_embedding(self) -> int:
        """Retorna la dimensión del vector de embedding."""
        pass
    
    @abstractmethod
    def obtener_modelo_usado(self) -> str:
        """Retorna el nombre del modelo de embedding usado."""
        pass