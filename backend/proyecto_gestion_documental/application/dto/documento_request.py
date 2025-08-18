from pydantic import BaseModel, validator
from typing import Optional


class DocumentoCreateRequest(BaseModel):
    """DTO para crear un nuevo documento."""
    
    titulo: str
    contenido: str
    tipo: str = "normativo"
    
    @validator('titulo')
    def validar_titulo(cls, v):
        if not v or not v.strip():
            raise ValueError('El título no puede estar vacío')
        if len(v.strip()) < 5:
            raise ValueError('El título debe tener al menos 5 caracteres')
        if len(v.strip()) > 200:
            raise ValueError('El título no puede exceder 200 caracteres')
        return v.strip()
    
    @validator('contenido')
    def validar_contenido(cls, v):
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        if len(v.strip()) < 50:
            raise ValueError('El contenido debe tener al menos 50 caracteres')
        return v.strip()
    
    @validator('tipo')
    def validar_tipo(cls, v):
        tipos_validos = ['normativo', 'procedimiento', 'manual', 'politica', 'otro']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()


class DocumentoUpdateRequest(BaseModel):
    """DTO para actualizar un documento existente."""
    
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    tipo: Optional[str] = None
    
    @validator('titulo')
    def validar_titulo(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('El título no puede estar vacío')
            if len(v.strip()) < 5:
                raise ValueError('El título debe tener al menos 5 caracteres')
            if len(v.strip()) > 200:
                raise ValueError('El título no puede exceder 200 caracteres')
            return v.strip()
        return v
    
    @validator('contenido')
    def validar_contenido(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('El contenido no puede estar vacío')
            if len(v.strip()) < 50:
                raise ValueError('El contenido debe tener al menos 50 caracteres')
            return v.strip()
        return v
    
    @validator('tipo')
    def validar_tipo(cls, v):
        if v is not None:
            tipos_validos = ['normativo', 'procedimiento', 'manual', 'politica', 'otro']
            if v.lower() not in tipos_validos:
                raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
            return v.lower()
        return v