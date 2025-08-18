from application.dto.auth_request import LoginRequest
from domain.repositories.usuario_repository import UsuarioRepository
from domain.services.password_service import PasswordService
from domain.services.jwt_service import JWTService

class LoginUserUseCase:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        password_service: PasswordService,
        jwt_service: JWTService
    ):
        self.usuario_repository = usuario_repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    async def execute(self, request: LoginRequest) -> str:
        # Buscar usuario usando tu método
        user = await self.usuario_repository.obtener_por_username(request.username)
        if not user:
            raise ValueError("Credenciales inválidas")
        
        # Verificar contraseña
        if not self.password_service.verify_password(request.password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        
        # Verificar si está activo
        if not user.is_active:
            raise ValueError("Usuario inactivo")
        
        # Crear token
        token = self.jwt_service.create_token(user.id, user.username)
        return token