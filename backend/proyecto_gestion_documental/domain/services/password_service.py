from abc import ABC, abstractmethod

class PasswordService(ABC):
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hashear contraseña"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        pass