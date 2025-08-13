#!/usr/bin/env python3
"""Script para iniciar el servidor FastAPI"""

if __name__ == "__main__":
    import uvicorn
    import os
    
    print("🚀 Iniciando servidor de Gestión Documental Inteligente...")
    print("📝 API Docs: http://localhost:8000/docs")
    print("🔧 Para detener: Ctrl+C")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")