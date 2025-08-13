# Backend - Gestión Documental Inteligente

Backend con FastAPI que implementa RAG (Retrieval-Augmented Generation) para consultas inteligentes sobre documentos normativos.

## 🚀 Características

- **FastAPI**: API REST rápida y moderna
- **ChromaDB**: Base de datos vectorial para búsquedas semánticas
- **Sentence Transformers**: Generación de embeddings para documentos
- **Ollama**: Integración con modelos LLM locales
- **CORS**: Configurado para aplicaciones Flutter

## 📋 Endpoints

### GET `/`
Estado de la API

### POST `/documentos/`
Subir un nuevo documento
```json
{
  "titulo": "Título del documento",
  "contenido": "Contenido completo...",
  "tipo": "normativo"
}
```

### GET `/documentos/`
Listar todos los documentos almacenados

### POST `/consultas/`
Realizar consulta con RAG
```json
{
  "pregunta": "¿Qué equipos de protección debo usar?",
  "limite_resultados": 5
}
```

## 🛠️ Instalación

1. **Crear entorno virtual:**
```bash
cd backend
cd Proyecto_gestion_documental
python -m venv doc_inteligente
source doc_inteligente/Scripts/activate  # Windows
 .\doc_inteligente\Scripts\Activate.ps1
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Instalar Ollama:**
- Descargar desde: https://ollama.ai/download/windows
- Instalar y ejecutar: `ollama serve`
- Descargar modelo: `ollama pull llama3.2:3b`

## 🚀 Uso

### Iniciar servidor
```bash
python start_server.py
```
O directamente:
```bash
python main.py
```

### Probar API
```bash
python test_api.py
```

### Documentación interactiva
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Configuración

- **Puerto**: 8000 (configurable en main.py)
- **Host**: 0.0.0.0 (accesible desde red local)
- **Modelo de embeddings**: all-MiniLM-L6-v2
- **Ollama URL**: http://localhost:11434

## 📁 Estructura

```
proyecto_gestion_documental/
├── main.py              # Aplicación FastAPI principal
├── start_server.py      # Script de inicio
├── test_api.py          # Pruebas de la API
├── test_packages.py     # Verificación de dependencias
├── requirements.txt     # Dependencias Python
└── README.md           # Este archivo
```

## 🧪 Pruebas

El archivo `test_api.py` incluye pruebas para:
- ✅ Estado de la API
- ✅ Subida de documentos
- ✅ Listado de documentos
- ✅ Consultas con RAG (requiere Ollama)

## 🔍 Troubleshooting

### Error: "No se puede conectar a la API"
- Verificar que el servidor esté corriendo
- Comprobar puerto 8000 disponible

### Error: "Error al consultar LLM"
- Verificar que Ollama esté corriendo: `ollama serve`
- Verificar que el modelo esté disponible: `ollama list`

### Error de embeddings
- Verificar conexión a internet (primera descarga del modelo)
- Verificar espacio en disco disponible