from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from application.use_cases.register_user_use_case import RegisterUserUseCase
from application.use_cases.login_user_use_case import LoginUserUseCase
from application.use_cases.verify_token_use_case import VerifyTokenUseCase
from application.dto.auth_request import RegisterRequest, LoginRequest
from application.dto.auth_response import AuthResponse, TokenResponse

class AuthController:
    def __init__(
        self,
        register_use_case: RegisterUserUseCase,
        login_use_case: LoginUserUseCase,
        verify_token_use_case: VerifyTokenUseCase
    ):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case
        self.verify_token_use_case = verify_token_use_case
        self.security = HTTPBearer()

    def get_router(self) -> APIRouter:
        router = APIRouter(prefix="/auth", tags=["Authentication"])
        
        @router.post("/register", response_model=AuthResponse)
        async def register(request: RegisterRequest):
            """Registrar nuevo usuario"""
            try:
                result = await self.register_use_case.execute(request)
                return AuthResponse(
                    success=True,
                    message="Usuario registrado exitosamente",
                    data=result
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @router.post("/login", response_model=TokenResponse)
        async def login(request: LoginRequest):
            """Iniciar sesión"""
            try:
                token = await self.login_use_case.execute(request)
                return TokenResponse(
                    access_token=token,
                    token_type="bearer"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )

        @router.get("/verify")
        async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(self.security)):
            """Verificar token"""
            try:
                user = await self.verify_token_use_case.execute(credentials.credentials)
                return {"user": user, "valid": True}
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )

        return router

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Dependency para obtener usuario actual"""
        try:
            return await self.verify_token_use_case.execute(credentials.credentials)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )