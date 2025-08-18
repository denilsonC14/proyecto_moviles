from typing import List, Optional
from ..dto.consulta_response import DocumentosListResponse, DocumentoPreviewResponse
from ...domain.entities.documento import Documento
from ...domain.repositories.documento_repository import DocumentoRepository


class ListDocumentsUseCase:
    """Caso de uso para listar documentos."""
    
    def __init__(self, documento_repository: DocumentoRepository):
        self.documento_repository = documento_repository
    
    async def execute(
        self, 
        pagina: Optional[int] = None, 
        limite: Optional[int] = None
    ) -> DocumentosListResponse:
        """
        Lista todos los documentos con paginación opcional.
        
        Args:
            pagina: Número de página (opcional)
            limite: Límite de documentos por página (opcional)
            
        Returns:
            DocumentosListResponse: Lista de documentos con metadatos
        """
        try:
            # Obtener todos los documentos del repositorio
            documentos = await self.documento_repository.obtener_todos()
            
            # Aplicar paginación si se especifica
            if pagina is not None and limite is not None:
                documentos_paginados = self._aplicar_paginacion(
                    documentos, pagina, limite
                )
            else:
                documentos_paginados = documentos
            
            # Convertir a DTOs de preview (sin contenido completo)
            documentos_preview = [
                self._documento_to_preview(doc) for doc in documentos_paginados
            ]
            
            # Obtener total de documentos
            total_documentos = len(documentos)
            
            return DocumentosListResponse(
                documentos=documentos_preview,
                total=total_documentos,
                pagina=pagina,
                limite=limite
            )
            
        except Exception as e:
            raise Exception(f"Error al listar documentos: {str(e)}")
    
    async def obtener_por_id(self, documento_id: str) -> Optional[DocumentoPreviewResponse]:
        """
        Obtiene un documento específico por su ID.
        
        Args:
            documento_id: ID del documento a buscar
            
        Returns:
            DocumentoPreviewResponse: Documento encontrado o None
        """
        try:
            documento = await self.documento_repository.obtener_por_id(documento_id)
            
            if documento is None:
                return None
            
            return self._documento_to_preview(documento)
            
        except Exception as e:
            raise Exception(f"Error al obtener documento {documento_id}: {str(e)}")
    
    def _aplicar_paginacion(
        self, 
        documentos: List[Documento], 
        pagina: int, 
        limite: int
    ) -> List[Documento]:
        """Aplica paginación a la lista de documentos."""
        if pagina < 1:
            pagina = 1
        if limite < 1:
            limite = 10
        
        inicio = (pagina - 1) * limite
        fin = inicio + limite
        
        return documentos[inicio:fin]
    
    def _documento_to_preview(self, documento: Documento) -> DocumentoPreviewResponse:
        """Convierte una entidad Documento a DocumentoPreviewResponse."""
        return DocumentoPreviewResponse(
            id=documento.id,
            titulo=documento.titulo,
            contenido_preview=documento.contenido_preview,
            tipo=documento.tipo,
            similitud=documento.similitud
        )