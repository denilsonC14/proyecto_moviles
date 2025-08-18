from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ...domain.entities.consulta import Usuario
from ...domain.repositories.usuario_repository import UsuarioRepository


# Definir modelo SQLAlchemy
Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)


class SQLiteUsuarioRepository(UsuarioRepository):
    """Implementación del repositorio de usuarios usando SQLite."""
    
    def __init__(self, database_url: str = "sqlite:///usuarios.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Crear tablas si no existen
        Base.metadata.create_all(bind=self.engine)
    
    def _get_session(self) -> Session:
        """Obtiene una sesión de base de datos."""
        return self.SessionLocal()
    
    async def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        try:
            with self._get_session() as db:
                usuario_model = db.query(UsuarioModel).filter(
                    UsuarioModel.id == usuario_id
                ).first()
                
                if usuario_model is None:
                    return None
                
                return self._convertir_a_entidad(usuario_model)
                
        except Exception as e:
            raise Exception(f"Error al obtener usuario por ID {usuario_id}: {str(e)}")
    
    async def obtener_por_username(self, username: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario."""
        try:
            with self._get_session() as db:
                usuario_model = db.query(UsuarioModel).filter(
                    UsuarioModel.username == username.lower()
                ).first()
                
                if usuario_model is None:
                    return None
                
                return self._convertir_a_entidad(usuario_model)
                
        except Exception as e:
            raise Exception(f"Error al obtener usuario por username {username}: {str(e)}")
    
    async def crear(self, usuario: Usuario) -> int:
        """Crea un nuevo usuario y retorna su ID."""
        try:
            with self._get_session() as db:
                usuario_model = UsuarioModel(
                    username=usuario.username.lower(),
                    hashed_password=usuario.hashed_password,
                    fecha_registro=usuario.fecha_registro or datetime.now()
                )
                
                db.add(usuario_model)
                db.commit()
                db.refresh(usuario_model)
                
                return usuario_model.id
                
        except IntegrityError:
            raise ValueError("El nombre de usuario ya existe")
        except Exception as e:
            raise Exception(f"Error al crear usuario: {str(e)}")
    
    async def actualizar(self, usuario: Usuario) -> bool:
        """Actualiza un usuario existente."""
        try:
            with self._get_session() as db:
                usuario_model = db.query(UsuarioModel).filter(
                    UsuarioModel.id == usuario.id
                ).first()
                
                if usuario_model is None:
                    return False
                
                usuario_model.username = usuario.username.lower()
                usuario_model.hashed_password = usuario.hashed_password
                
                db.commit()
                return True
                
        except IntegrityError:
            raise ValueError("El nombre de usuario ya existe")
        except Exception as e:
            raise Exception(f"Error al actualizar usuario: {str(e)}")
    
    async def eliminar(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        try:
            with self._get_session() as db:
                usuario_model = db.query(UsuarioModel).filter(
                    UsuarioModel.id == usuario_id
                ).first()
                
                if usuario_model is None:
                    return False
                
                db.delete(usuario_model)
                db.commit()
                return True
                
        except Exception as e:
            raise Exception(f"Error al eliminar usuario {usuario_id}: {str(e)}")
    
    async def existe_username(self, username: str) -> bool:
        """Verifica si un nombre de usuario ya existe."""
        try:
            with self._get_session() as db:
                usuario_existe = db.query(UsuarioModel).filter(
                    UsuarioModel.username == username.lower()
                ).first() is not None
                
                return usuario_existe
                
        except Exception as e:
            raise Exception(f"Error al verificar existencia de username {username}: {str(e)}")
    
    def _convertir_a_entidad(self, usuario_model: UsuarioModel) -> Usuario:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        return Usuario(
            id=usuario_model.id,
            username=usuario_model.username,
            hashed_password=usuario_model.hashed_password,
            fecha_registro=usuario_model.fecha_registro
        )