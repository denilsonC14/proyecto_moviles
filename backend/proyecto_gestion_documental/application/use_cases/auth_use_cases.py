from typing import Optional
from passlib.context import CryptContext
from ..dto.auth_dto import (
    UsuarioCreateRequest, 
    UsuarioLoginRequest, 
    AuthResponse, 
    UsuarioResponse
)
from ...domain.entities.consulta import Usuario
from ...domain.repositories.usuario_repository import UsuarioRepository


class RegisterUserUseCase:
    """Caso de uso para registrar un nuevo usuario."""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, request: UsuarioCreateRequest) -> AuthResponse:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            request: Datos del usuario a registrar
            
        Returns:
            AuthResponse: Respuesta con información del usuario creado
            
        Raises:
            ValueError: Si el usuario ya existe o datos inválidos
            Exception: Si hay errores durante el registro
        """
        try:
            # Verificar si el usuario ya existe
            usuario_existente = await self.usuario_repository.obtener_por_username(
                request.username
            )
            
            if usuario_existente is not None:
                raise ValueError("El nombre de usuario ya está en uso")
            
            # Crear hash de la contraseña
            hashed_password = self._hash_password(request.password)
            
            # Crear entidad de usuario (sin ID, se generará en el repositorio)
            usuario = Usuario(
                id=0,  # Se asignará en el repositorio
                username=request.username,
                hashed_password=hashed_password
            )
            
            # Validar usuario según reglas de dominio
            if not usuario.es_valido():
                raise ValueError("El usuario no cumple con las reglas de validación")
            
            # Guardar usuario
            usuario_id = await self.usuario_repository.crear(usuario)
            usuario.id = usuario_id
            
            # Preparar respuesta
            usuario_response = UsuarioResponse(
                id=usuario.id,
                username=usuario.username,
                fecha_registro=usuario.fecha_registro.isoformat() if usuario.fecha_registro else None
            )
            
            return AuthResponse(
                mensaje="Usuario registrado exitosamente",
                usuario=usuario_response
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error al registrar usuario: {str(e)}")
    
    def _hash_password(self, password: str) -> str:
        """Genera hash de la contraseña."""
        return self.pwd_context.hash(password)


class LoginUserUseCase:
    """Caso de uso para autenticar un usuario."""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, request: UsuarioLoginRequest) -> AuthResponse:
        """
        Autentica un usuario en el sistema.
        
        Args:
            request: Credenciales del usuario
            
        Returns:
            AuthResponse: Respuesta con información del usuario autenticado
            
        Raises:
            ValueError: Si las credenciales son inválidas
            Exception: Si hay errores durante la autenticación
        """
        try:
            # Buscar usuario por username
            usuario = await self.usuario_repository.obtener_por_username(
                request.username
            )
            
            if usuario is None:
                raise ValueError("Credenciales inválidas")
            
            # Verificar contraseña
            if not self._verify_password(request.password, usuario.hashed_password):
                raise ValueError("Credenciales inválidas")
            
            # Preparar respuesta
            usuario_response = UsuarioResponse(
                id=usuario.id,
                username=usuario.username,
                fecha_registro=usuario.fecha_registro.isoformat() if usuario.fecha_registro else None
            )
            
            return AuthResponse(
                mensaje="Login exitoso",
                usuario=usuario_response
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error durante el login: {str(e)}")
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash."""
        return self.pwd_context.verify(plain_password, hashed_password)