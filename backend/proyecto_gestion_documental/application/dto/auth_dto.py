from pydantic import BaseModel, validator
from typing import Optional


class UsuarioCreateRequest(BaseModel):
    """DTO para crear un nuevo usuario."""
    
    username: str
    password: str
    
    @validator('username')
    def validar_username(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        if len(v.strip()) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if len(v.strip()) > 30:
            raise ValueError('El nombre de usuario no puede exceder 30 caracteres')
        # Solo permitir letras, números y guiones bajos
        if not v.strip().replace('_', '').isalnum():
            raise ValueError('El nombre de usuario solo puede contener letras, números y guiones bajos')
        return v.strip().lower()
    
    @validator('password')
    def validar_password(cls, v):
        if not v:
            raise ValueError('La contraseña no puede estar vacía')
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        if len(v) > 100:
            raise ValueError('La contraseña no puede exceder 100 caracteres')
        return v


class UsuarioLoginRequest(BaseModel):
    """DTO para login de usuario."""
    
    username: str
    password: str
    
    @validator('username')
    def validar_username(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        return v.strip().lower()
    
    @validator('password')
    def validar_password(cls, v):
        if not v:
            raise ValueError('La contraseña no puede estar vacía')
        return v


class UsuarioResponse(BaseModel):
    """DTO para respuesta de usuario."""
    
    id: int
    username: str
    fecha_registro: Optional[str] = None
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """DTO para respuesta de autenticación."""
    
    mensaje: str
    usuario: UsuarioResponse
    token: Optional[str] = None  # Para futuras implementaciones con JWT