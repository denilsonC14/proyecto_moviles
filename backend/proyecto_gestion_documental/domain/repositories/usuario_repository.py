from abc import ABC, abstractmethod
from typing import Optional
from ..entities.consulta import Usuario


class UsuarioRepository(ABC):
    """Interface para el repositorio de usuarios."""
    
    @abstractmethod
    async def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        pass
    
    @abstractmethod
    async def obtener_por_username(self, username: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario."""
        pass
    
    @abstractmethod
    async def crear(self, usuario: Usuario) -> int:
        """Crea un nuevo usuario y retorna su ID."""
        pass
    
    @abstractmethod
    async def actualizar(self, usuario: Usuario) -> bool:
        """Actualiza un usuario existente."""
        pass
    
    @abstractmethod
    async def eliminar(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        pass
    
    @abstractmethod
    async def existe_username(self, username: str) -> bool:
        """Verifica si un nombre de usuario ya existe."""
        pass