from application.dto.auth_request import RegisterRequest
from application.dto.auth_response import UserResponse
from domain.entities.usuario import Usuario
from domain.repositories.usuario_repository import UsuarioRepository
from domain.services.password_service import PasswordService

class RegisterUserUseCase:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        password_service: PasswordService
    ):
        self.usuario_repository = usuario_repository
        self.password_service = password_service
    
    async def execute(self, request: RegisterRequest) -> UserResponse:
        # Verificar si el usuario ya existe usando tu método
        if await self.usuario_repository.existe_username(request.username):
            raise ValueError("El usuario ya existe")
        
        # Hashear contraseña
        hashed_password = self.password_service.hash_password(request.password)
        
        # Crear usuario
        usuario = Usuario(
            username=request.username,
            hashed_password=hashed_password
        )
        
        # Guardar en repositorio usando tu método
        user_id = await self.usuario_repository.crear(usuario)
        usuario.id = user_id
        
        return UserResponse(
            id=usuario.id,
            username=usuario.username,
            is_active=usuario.is_active,
            created_at=usuario.created_at.isoformat()
        )