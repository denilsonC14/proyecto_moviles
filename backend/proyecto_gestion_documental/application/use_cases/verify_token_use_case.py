from typing import Optional
from application.dto.auth_response import UserTokenData
from domain.repositories.usuario_repository import UsuarioRepository
from domain.services.jwt_service import JWTService

class VerifyTokenUseCase:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        jwt_service: JWTService
    ):
        self.usuario_repository = usuario_repository
        self.jwt_service = jwt_service
    
    async def execute(self, token: str) -> UserTokenData:
        # Verificar token
        token_data = self.jwt_service.verify_token(token)
        if not token_data:
            raise ValueError("Token inválido")
        
        # Obtener usuario usando tu método
        user = await self.usuario_repository.obtener_por_id(token_data.get("user_id"))
        if not user or not user.is_active:
            raise ValueError("Usuario no encontrado o inactivo")
        
        return UserTokenData(
            user_id=user.id,
            username=user.username,
            is_active=user.is_active
        )