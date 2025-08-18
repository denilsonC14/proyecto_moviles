from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import chromadb
from sentence_transformers import SentenceTransformer
import requests
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext

app = FastAPI(title="Gestión Documental Inteligente API")

# CORS para Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de base de datos para usuarios
engine = create_engine("sqlite:///usuarios.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo de Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Inicializar modelos
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="documentos_normativos")

# Modelos Pydantic
class DocumentoRequest(BaseModel):
    titulo: str
    contenido: str
    tipo: str = "normativo"

class ConsultaRequest(BaseModel):
    pregunta: str
    limite_resultados: int = 5

class RespuestaDocumento(BaseModel):
    id: str
    titulo: str
    contenido: str
    similitud: float

class RespuestaConsulta(BaseModel):
    respuesta_ia: str
    documentos_relevantes: List[RespuestaDocumento]

# Modelos de Autenticación
class UsuarioCreate(BaseModel):
    username: str
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str

# Funciones auxiliares
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def consultar_ollama(prompt: str) -> str:
    """Consulta al modelo Llama via Ollama"""
    try:
        import ollama
        response = ollama.generate(
            model='llama3.2:1b',
            prompt=prompt
        )
        return response['response']
    except Exception as e:
        # Fallback to REST API
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error HTTP {response.status_code}: {response.text}"
        except requests.exceptions.ConnectionError:
            return "Error: Ollama no está corriendo. Ejecute 'ollama serve' en otra terminal."
        except Exception as e2:
            return f"Error al consultar LLM: {str(e)} | Fallback error: {str(e2)}"

@app.post("/documentos/", summary="Subir nuevo documento")
async def subir_documento(documento: DocumentoRequest):
    """Sube un documento y lo vectoriza para búsquedas"""
    try:
        # Generar embedding
        embedding = embedding_model.encode([documento.contenido])
        
        # Guardar en ChromaDB
        doc_id = f"doc_{len(collection.get()['ids']) + 1}"
        collection.add(
            embeddings=embedding.tolist(),
            documents=[documento.contenido],
            metadatas=[{
                "titulo": documento.titulo,
                "tipo": documento.tipo
            }],
            ids=[doc_id]
        )
        
        return {"mensaje": "Documento subido exitosamente", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consultas/", response_model=RespuestaConsulta)
async def realizar_consulta(consulta: ConsultaRequest):
    """Realiza búsqueda semántica y genera respuesta con LLM"""
    try:
        # 1. Vectorizar consulta
        query_embedding = embedding_model.encode([consulta.pregunta])
        
        # 2. Búsqueda en ChromaDB
        resultados = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=consulta.limite_resultados
        )
        
        # 3. Preparar contexto para LLM
        contexto = ""
        documentos_relevantes = []
        
        for i, doc in enumerate(resultados['documents'][0]):
            metadata = resultados['metadatas'][0][i]
            similitud = 1 - resultados['distances'][0][i]  # Convertir distancia a similitud
            
            contexto += f"Documento {i+1} - {metadata['titulo']}:\n{doc[:500]}...\n\n"
            
            documentos_relevantes.append(RespuestaDocumento(
                id=resultados['ids'][0][i],
                titulo=metadata['titulo'],
                contenido=doc[:200] + "...",
                similitud=round(similitud, 3)
            ))
        
        # 4. Generar respuesta con LLM
        prompt = f"""
        Contexto de documentos normativos:
        {contexto}
        
        Pregunta del usuario: {consulta.pregunta}
        
        Instrucciones:
        - Responde basándote ÚNICAMENTE en el contexto proporcionado
        - Si no encuentras información relevante, dilo claramente
        - Mantén una respuesta concisa y profesional
        - Cita las fuentes cuando sea posible
        
        Respuesta:
        """
        
        respuesta_ia = consultar_ollama(prompt)
        
        return RespuestaConsulta(
            respuesta_ia=respuesta_ia,
            documentos_relevantes=documentos_relevantes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documentos/", summary="Listar todos los documentos")
async def listar_documentos():
    """Lista todos los documentos almacenados"""
    try:
        datos = collection.get()
        documentos = []
        
        for i, doc_id in enumerate(datos['ids']):
            documentos.append({
                "id": doc_id,
                "titulo": datos['metadatas'][i]['titulo'],
                "tipo": datos['metadatas'][i]['tipo'],
                "contenido_preview": datos['documents'][i][:100] + "..."
            })
        
        return {"documentos": documentos, "total": len(documentos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints de Autenticación
@app.post("/register", summary="Registrar nuevo usuario")
async def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""
    try:
        # Verificar si usuario ya existe
        db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()
        if db_usuario:
            raise HTTPException(status_code=400, detail="Usuario ya existe")
        
        # Crear nuevo usuario
        hashed_password = pwd_context.hash(usuario.password)
        db_usuario = Usuario(username=usuario.username, hashed_password=hashed_password)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return {
            "mensaje": "Usuario registrado exitosamente",
            "usuario": {"id": db_usuario.id, "username": db_usuario.username}
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login", summary="Iniciar sesión")
async def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    """Autentica un usuario"""
    try:
        # Buscar usuario
        db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()
        if not db_usuario or not pwd_context.verify(usuario.password, db_usuario.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return {
            "mensaje": "Login exitoso",
            "usuario": {"id": db_usuario.id, "username": db_usuario.username}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", summary="Estado de la API")
async def root():
    return {
        "mensaje": "API de Gestión Documental Inteligente", 
        "estado": "activo",
        "version": "1.0.0",
        "endpoints": {
            "documentos": "/documentos/",
            "consultas": "/consultas/",
            "login": "/login",
            "register": "/register"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)