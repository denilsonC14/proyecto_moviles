from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ....application.use_cases.upload_document_use_case import UploadDocumentUseCase
from ....application.use_cases.search_documents_use_case import SearchDocumentsUseCase
from ....application.use_cases.list_documents_use_case import ListDocumentsUseCase
from ....application.dto.documento_request import DocumentoCreateRequest
from ....application.dto.consulta_response import (
    ConsultaRequest, 
    ConsultaResponse, 
    DocumentoCreateResponse,
    DocumentosListResponse
)


class DocumentoController:
    """Controlador para operaciones relacionadas con documentos."""
    
    def __init__(
        self,
        upload_use_case: UploadDocumentUseCase,
        search_use_case: SearchDocumentsUseCase,
        list_use_case: ListDocumentsUseCase
    ):
        self.upload_use_case = upload_use_case
        self.search_use_case = search_use_case
        self.list_use_case = list_use_case
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas del controlador."""
        
        @self.router.post(
            "/documentos/", 
            response_model=DocumentoCreateResponse,
            summary="Subir nuevo documento"
        )
        async def subir_documento(documento: DocumentoCreateRequest):
            """Sube un documento y lo vectoriza para búsquedas."""
            try:
                resultado = await self.upload_use_case.execute(documento)
                return resultado
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post(
            "/consultas/", 
            response_model=ConsultaResponse,
            summary="Realizar consulta con RAG"
        )
        async def realizar_consulta(consulta: ConsultaRequest):
            """Realiza búsqueda semántica y genera respuesta con LLM."""
            try:
                resultado = await self.search_use_case.execute(consulta)
                return resultado
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get(
            "/documentos/", 
            response_model=DocumentosListResponse,
            summary="Listar todos los documentos"
        )
        async def listar_documentos(
            pagina: Optional[int] = None,
            limite: Optional[int] = None
        ):
            """Lista todos los documentos almacenados con paginación opcional."""
            try:
                resultado = await self.list_use_case.execute(pagina, limite)
                return resultado
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get(
            "/documentos/{documento_id}",
            summary="Obtener documento por ID"
        )
        async def obtener_documento(documento_id: str):
            """Obtiene un documento específico por su ID."""
            try:
                documento = await self.list_use_case.obtener_por_id(documento_id)
                
                if documento is None:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Documento {documento_id} no encontrado"
                    )
                
                return documento
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Retorna el router configurado."""
        return self.router