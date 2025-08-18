from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DocumentoResponse(BaseModel):
    """DTO para respuesta de documento."""
    
    id: str
    titulo: str
    contenido: str
    tipo: str
    similitud: Optional[float] = None
    fecha_creacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DocumentoPreviewResponse(BaseModel):
    """DTO para vista previa de documento."""
    
    id: str
    titulo: str
    contenido_preview: str
    tipo: str
    similitud: Optional[float] = None
    
    class Config:
        from_attributes = True


class ConsultaRequest(BaseModel):
    """DTO para petición de consulta."""
    
    pregunta: str
    limite_resultados: int = 5
    
    def validar(self):
        if not self.pregunta or not self.pregunta.strip():
            raise ValueError('La pregunta no puede estar vacía')
        if self.limite_resultados <= 0 or self.limite_resultados > 20:
            raise ValueError('El límite de resultados debe estar entre 1 y 20')


class ConsultaResponse(BaseModel):
    """DTO para respuesta de consulta."""
    
    respuesta_ia: str
    documentos_relevantes: List[DocumentoResponse]
    pregunta_original: str
    tiempo_procesamiento: Optional[float] = None
    modelo_usado: Optional[str] = None
    
    @property
    def numero_documentos(self) -> int:
        return len(self.documentos_relevantes)
    
    @property
    def tiene_documentos_relevantes(self) -> bool:
        return self.numero_documentos > 0


class DocumentoCreateResponse(BaseModel):
    """DTO para respuesta de creación de documento."""
    
    mensaje: str
    id: str
    titulo: str


class DocumentosListResponse(BaseModel):
    """DTO para respuesta de lista de documentos."""
    
    documentos: List[DocumentoPreviewResponse]
    total: int
    pagina: Optional[int] = None
    limite: Optional[int] = None