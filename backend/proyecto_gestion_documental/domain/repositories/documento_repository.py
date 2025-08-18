from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.documento import Documento


class DocumentoRepository(ABC):
    """Interface para el repositorio de documentos."""
    
    @abstractmethod
    async def obtener_por_id(self, documento_id: str) -> Optional[Documento]:
        """Obtiene un documento por su ID."""
        pass
    
    @abstractmethod
    async def obtener_todos(self) -> List[Documento]:
        """Obtiene todos los documentos almacenados."""
        pass
    
    @abstractmethod
    async def guardar(self, documento: Documento) -> str:
        """Guarda un documento y retorna su ID."""
        pass
    
    @abstractmethod
    async def eliminar(self, documento_id: str) -> bool:
        """Elimina un documento por su ID."""
        pass
    
    @abstractmethod
    async def buscar_por_similitud(
        self, 
        embedding: List[float], 
        limite: int = 5
    ) -> List[Documento]:
        """Busca documentos similares basándose en un embedding."""
        pass
    
    @abstractmethod
    async def contar_documentos(self) -> int:
        """Cuenta el número total de documentos."""
        pass