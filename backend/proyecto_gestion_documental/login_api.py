from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext

app = FastAPI(title="API de Login con SQLite")

# Configuración de la base de datos SQLite
engine = create_engine("sqlite:///usuarios.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

class UsuarioCreate(BaseModel):
    username: str
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(usuario.password)
    db_usuario = Usuario(username=usuario.username, hashed_password=hashed_password)
    db.add(db_usuario)
    try:
        db.commit()
        db.refresh(db_usuario)
        return {"mensaje": "Usuario registrado"}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuario ya existe")

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if not db_usuario or not pwd_context.verify(usuario.password, db_usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"mensaje": "Login exitoso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
