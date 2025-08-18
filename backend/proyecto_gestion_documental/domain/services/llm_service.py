from abc import ABC, abstractmethod
from typing import Optional


class LLMService(ABC):
    """Interface para servicios de Large Language Models."""
    
    @abstractmethod
    async def generar_respuesta(
        self, 
        prompt: str, 
        contexto: Optional[str] = None
    ) -> str:
        """
        Genera una respuesta usando un modelo de lenguaje.
        
        Args:
            prompt: La pregunta o prompt para el modelo
            contexto: Contexto adicional para mejorar la respuesta
            
        Returns:
            str: La respuesta generada por el modelo
        """
        pass
    
    @abstractmethod
    async def esta_disponible(self) -> bool:
        """Verifica si el servicio LLM está disponible."""
        pass
    
    @abstractmethod
    def obtener_modelo_usado(self) -> str:
        """Retorna el nombre del modelo que se está usando."""
        pass