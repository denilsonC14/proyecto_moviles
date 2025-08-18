from typing import List
import asyncio
from sentence_transformers import SentenceTransformer
from ...domain.services.embedding_service import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):
    """Implementación del servicio de embeddings usando SentenceTransformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        self._dimension = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Inicializa el modelo de embeddings."""
        try:
            self.model = SentenceTransformer(self.model_name)
            # Calcular dimensión usando un texto de prueba
            test_embedding = self.model.encode(["test"])
            self._dimension = len(test_embedding[0])
        except Exception as e:
            raise Exception(f"Error inicializando modelo de embeddings {self.model_name}: {str(e)}")
    
    async def generar_embedding(self, texto: str) -> List[float]:
        """
        Genera un embedding vectorial para un texto.
        
        Args:
            texto: El texto para el cual generar el embedding
            
        Returns:
            List[float]: Vector de embedding del texto
        """
        if not texto or not texto.strip():
            raise ValueError("El texto no puede estar vacío")
        
        try:
            # Ejecutar encoding en un hilo separado para no bloquear
            def _encode():
                embedding = self.model.encode([texto.strip()])
                return embedding[0].tolist()
            
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(None, _encode)
            return embedding
            
        except Exception as e:
            raise Exception(f"Error generando embedding: {str(e)}")
    
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
        if not textos:
            return []
        
        # Filtrar textos vacíos
        textos_validos = [texto.strip() for texto in textos if texto and texto.strip()]
        
        if not textos_validos:
            raise ValueError("No hay textos válidos para procesar")
        
        try:
            # Ejecutar encoding batch en un hilo separado
            def _encode_batch():
                embeddings = self.model.encode(textos_validos)
                return [embedding.tolist() for embedding in embeddings]
            
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(None, _encode_batch)
            return embeddings
            
        except Exception as e:
            raise Exception(f"Error generando embeddings batch: {str(e)}")
    
    def obtener_dimension_embedding(self) -> int:
        """Retorna la dimensión del vector de embedding."""
        if self._dimension is None:
            raise Exception("Modelo no inicializado correctamente")
        return self._dimension
    
    def obtener_modelo_usado(self) -> str:
        """Retorna el nombre del modelo de embedding usado."""
        return self.model_name
    
    def es_modelo_valido(self, model_name: str) -> bool:
        """Verifica si un nombre de modelo es válido."""
        modelos_comunes = [
            'all-MiniLM-L6-v2',
            'all-MiniLM-L12-v2',
            'all-mpnet-base-v2',
            'multi-qa-MiniLM-L6-cos-v1',
            'multi-qa-mpnet-base-dot-v1',
            'paraphrase-MiniLM-L6-v2',
            'paraphrase-multilingual-MiniLM-L12-v2'
        ]
        return model_name in modelos_comunes
    
    async def cambiar_modelo(self, nuevo_modelo: str) -> bool:
        """
        Cambia el modelo de embeddings utilizado.
        
        Args:
            nuevo_modelo: Nombre del nuevo modelo a usar
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        try:
            # Guardar modelo anterior en caso de error
            modelo_anterior = self.model
            modelo_anterior_nombre = self.model_name
            dimension_anterior = self._dimension
            
            # Intentar cargar nuevo modelo
            self.model_name = nuevo_modelo
            self._initialize_model()
            
            return True
            
        except Exception as e:
            # Restaurar modelo anterior si hay error
            self.model = modelo_anterior
            self.model_name = modelo_anterior_nombre
            self._dimension = dimension_anterior
            raise Exception(f"Error cambiando modelo a {nuevo_modelo}: {str(e)}")
    
    def obtener_informacion_modelo(self) -> dict:
        """Retorna información detallada del modelo actual."""
        return {
            "nombre": self.model_name,
            "dimension": self._dimension,
            "inicializado": self.model is not None,
            "tipo": "SentenceTransformer"
        }