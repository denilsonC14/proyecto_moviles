from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.token import Token

class JWTService(ABC):
    
    @abstractmethod
    def create_token(self, user_id: int, username: str) -> str:
        """Crear token JWT"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        """Verificar y decodificar token JWT"""
        pass
    
    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decodificar token sin verificar"""
        pass