import time
from typing import List
from ..dto.consulta_response import ConsultaRequest, ConsultaResponse, DocumentoResponse
from ...domain.entities.documento import Documento
from ...domain.entities.consulta import Consulta, ResultadoConsulta
from ...domain.repositories.documento_repository import DocumentoRepository
from ...domain.services.embedding_service import EmbeddingService
from ...domain.services.llm_service import LLMService


class SearchDocumentsUseCase:
    """Caso de uso para buscar documentos usando RAG."""
    
    def __init__(
        self,
        documento_repository: DocumentoRepository,
        embedding_service: EmbeddingService,
        llm_service: LLMService
    ):
        self.documento_repository = documento_repository
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    async def execute(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Ejecuta una búsqueda con RAG (Retrieval-Augmented Generation).
        
        Args:
            request: Petición de consulta con pregunta y límite de resultados
            
        Returns:
            ConsultaResponse: Respuesta con documentos relevantes y respuesta de IA
        """
        inicio_tiempo = time.time()
        
        try:
            # Validar request
            request.validar()
            
            # Crear entidad de consulta
            consulta = Consulta(
                pregunta=request.pregunta,
                limite_resultados=request.limite_resultados
            )
            
            # Validar consulta según reglas de dominio
            if not consulta.es_valida():
                raise ValueError("La consulta no cumple con las reglas de validación")
            
            # 1. Generar embedding de la pregunta
            embedding_pregunta = await self.embedding_service.generar_embedding(
                consulta.pregunta
            )
            
            # 2. Buscar documentos similares
            documentos_similares = await self.documento_repository.buscar_por_similitud(
                embedding_pregunta, 
                consulta.limite_resultados
            )
            
            # 3. Preparar contexto para LLM
            contexto = self._preparar_contexto(documentos_similares)
            
            # 4. Generar respuesta con LLM
            prompt = self._construir_prompt(consulta.pregunta, contexto)
            respuesta_ia = await self.llm_service.generar_respuesta(prompt)
            
            # 5. Calcular tiempo de procesamiento
            tiempo_procesamiento = time.time() - inicio_tiempo
            
            # 6. Convertir documentos a DTOs
            documentos_response = [
                self._documento_to_response(doc) for doc in documentos_similares
            ]
            
            return ConsultaResponse(
                respuesta_ia=respuesta_ia,
                documentos_relevantes=documentos_response,
                pregunta_original=consulta.pregunta,
                tiempo_procesamiento=tiempo_procesamiento,
                modelo_usado=self.llm_service.obtener_modelo_usado()
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error durante la búsqueda: {str(e)}")
    
    def _preparar_contexto(self, documentos: List[Documento]) -> str:
        """Prepara el contexto a partir de los documentos relevantes."""
        if not documentos:
            return "No se encontraron documentos relevantes."
        
        contexto_partes = []
        for i, doc in enumerate(documentos, 1):
            # Limitar contenido para no exceder límites del LLM
            contenido_limitado = doc.contenido[:500] if len(doc.contenido) > 500 else doc.contenido
            contexto_partes.append(
                f"Documento {i} - {doc.titulo}:\n{contenido_limitado}\n"
            )
        
        return "\n".join(contexto_partes)
    
    def _construir_prompt(self, pregunta: str, contexto: str) -> str:
        """Construye el prompt para el modelo LLM."""
        return f"""
Contexto de documentos normativos:
{contexto}

Pregunta del usuario: {pregunta}

Instrucciones:
- Responde basándote ÚNICAMENTE en el contexto proporcionado
- Si no encuentras información relevante en el contexto, dilo claramente
- Mantén una respuesta concisa y profesional
- Cita las fuentes cuando sea posible mencionando el número del documento
- No agregues información que no esté en el contexto

Respuesta:
"""
    
    def _documento_to_response(self, documento: Documento) -> DocumentoResponse:
        """Convierte una entidad Documento a DocumentoResponse."""
        return DocumentoResponse(
            id=documento.id,
            titulo=documento.titulo,
            contenido=documento.contenido,
            tipo=documento.tipo,
            similitud=documento.similitud,
            fecha_creacion=documento.fecha_creacion
        )