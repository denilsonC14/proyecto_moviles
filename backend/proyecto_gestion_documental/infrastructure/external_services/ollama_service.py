from typing import Optional
import requests
import asyncio
from ...domain.services.llm_service import LLMService


class OllamaLLMService(LLMService):
    """Implementación del servicio LLM usando Ollama."""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:11434",
        model_name: str = "llama3.2:1b",
        timeout: int = 30
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.timeout = timeout
    
    async def generar_respuesta(
        self, 
        prompt: str, 
        contexto: Optional[str] = None
    ) -> str:
        """
        Genera una respuesta usando Ollama.
        
        Args:
            prompt: El prompt para el modelo
            contexto: Contexto adicional (ya incluido en el prompt)
            
        Returns:
            str: Respuesta generada por el modelo
        """
        try:
            # Intentar usar librería ollama primero
            response = await self._try_ollama_library(prompt)
            if response:
                return response
                
            # Fallback a API REST
            return await self._try_rest_api(prompt)
            
        except Exception as e:
            return f"Error al consultar LLM: {str(e)}"
    
    async def esta_disponible(self) -> bool:
        """Verifica si el servicio Ollama está disponible."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def obtener_modelo_usado(self) -> str:
        """Retorna el nombre del modelo que se está usando."""
        return self.model_name
    
    async def _try_ollama_library(self, prompt: str) -> Optional[str]:
        """Intenta usar la librería ollama directamente."""
        try:
            import ollama
            
            # Ejecutar en un hilo separado para no bloquear
            def _generate():
                response = ollama.generate(
                    model=self.model_name,
                    prompt=prompt
                )
                return response['response']
            
            # Ejecutar de forma asíncrona
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _generate)
            return response
            
        except ImportError:
            # La librería ollama no está disponible
            return None
        except Exception as e:
            # Error con la librería, intentar API REST
            return None
    
    async def _try_rest_api(self, prompt: str) -> str:
        """Usa la API REST de Ollama como fallback."""
        try:
            def _make_request():
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response.json()["response"]
                else:
                    raise Exception(f"Error HTTP {response.status_code}: {response.text}")
            
            # Ejecutar de forma asíncrona
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _make_request)
            return response
            
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama no está corriendo. Ejecute 'ollama serve' en otra terminal.")
        except requests.exceptions.Timeout:
            raise Exception("Timeout al conectar con Ollama. El modelo puede estar cargándose.")
        except Exception as e:
            raise Exception(f"Error en API REST de Ollama: {str(e)}")
    
    async def configurar_modelo(self, model_name: str) -> bool:
        """Configura un modelo específico para usar."""
        try:
            # Verificar que el modelo existe
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if model_name in model_names:
                    self.model_name = model_name
                    return True
                else:
                    available_models = ", ".join(model_names)
                    raise Exception(f"Modelo {model_name} no encontrado. Disponibles: {available_models}")
            
            return False
            
        except Exception as e:
            raise Exception(f"Error configurando modelo: {str(e)}")
    
    async def listar_modelos_disponibles(self) -> list:
        """Lista los modelos disponibles en Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
            
        except Exception:
            return []