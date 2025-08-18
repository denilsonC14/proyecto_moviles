import uuid
from typing import Optional
from ..dto.documento_request import DocumentoCreateRequest
from ..dto.consulta_response import DocumentoCreateResponse
from ...domain.entities.documento import Documento
from ...domain.repositories.documento_repository import DocumentoRepository
from ...domain.services.embedding_service import EmbeddingService


class UploadDocumentUseCase:
    """Caso de uso para subir un nuevo documento."""
    
    def __init__(
        self, 
        documento_repository: DocumentoRepository,
        embedding_service: EmbeddingService
    ):
        self.documento_repository = documento_repository
        self.embedding_service = embedding_service
    
    async def execute(self, request: DocumentoCreateRequest) -> DocumentoCreateResponse:
        """
        Ejecuta el caso de uso de subir documento.
        
        Args:
            request: Datos del documento a crear
            
        Returns:
            DocumentoCreateResponse: Respuesta con información del documento creado
            
        Raises:
            ValueError: Si los datos del documento no son válidos
            Exception: Si hay errores durante el proceso de creación
        """
        try:
            # Generar ID único para el documento
            documento_id = self._generar_id_documento()
            
            # Crear entidad de dominio
            documento = Documento(
                id=documento_id,
                titulo=request.titulo,
                contenido=request.contenido,
                tipo=request.tipo
            )
            
            # Validar que el documento sea válido según reglas de dominio
            if not documento.es_valido():
                raise ValueError("El documento no cumple con las reglas de validación de dominio")
            
            # Guardar documento en repositorio (que incluye generar y almacenar embedding)
            documento_id_guardado = await self.documento_repository.guardar(documento)
            
            return DocumentoCreateResponse(
                mensaje="Documento subido exitosamente",
                id=documento_id_guardado,
                titulo=documento.titulo
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error al subir documento: {str(e)}")
    
    def _generar_id_documento(self) -> str:
        """Genera un ID único para el documento."""
        return f"doc_{uuid.uuid4().hex[:8]}"
    
    async def _validar_documento_unico(self, titulo: str) -> bool:
        """
        Valida si ya existe un documento con el mismo título.
        Esto es opcional según las reglas de negocio.
        """
        # Implementar si se requiere validación de unicidad
        return True