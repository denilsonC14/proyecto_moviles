#!/usr/bin/env python3
"""Script para verificar el estado de Ollama"""

import requests
import json

def check_ollama_server():
    """Verifica si el servidor Ollama está corriendo"""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            print("[OK] Ollama servidor está corriendo")
            print(f"   Versión: {response.json()}")
            return True
        else:
            print(f"[ERROR] Ollama responde con error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Ollama no está corriendo")
        print("   Para iniciarlo: ollama serve")
        return False
    except Exception as e:
        print(f"[ERROR] Error verificando Ollama: {e}")
        return False

def check_available_models():
    """Lista los modelos disponibles en Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"[MODELS] Modelos disponibles ({len(models)}):")
            for model in models:
                print(f"   - {model['name']} (tamaño: {model.get('size', 'desconocido')})")
            return models
        else:
            print(f"[ERROR] Error obteniendo modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"[ERROR] Error listando modelos: {e}")
        return []

def test_model_query():
    """Prueba una consulta simple con el modelo"""
    try:
        # Intentar con llama3.2:3b primero
        models_to_try = ["llama3.2:1b", "llama3.2:3b", "llama3.2", "llama3", "llama3:8b"]
        
        for model in models_to_try:
            print(f"[TEST] Probando modelo: {model}")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": "Hola, ¿cómo estás? Responde en español brevemente.",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"[OK] Modelo {model} funciona correctamente")
                print(f"   Respuesta: {result['response'][:100]}...")
                return model
            else:
                print(f"[ERROR] Modelo {model} falló: {response.status_code}")
                
        print("[ERROR] Ningún modelo funcionó")
        return None
        
    except Exception as e:
        print(f"[ERROR] Error probando modelos: {e}")
        return None

def main():
    print("Verificando estado de Ollama...")
    print("=" * 50)
    
    # Verificar servidor
    if not check_ollama_server():
        print("\nPara instalar Ollama:")
        print("   1. Descargar: https://ollama.ai/download/windows")
        print("   2. Instalar el archivo .exe")
        print("   3. Ejecutar: ollama serve")
        print("   4. Descargar modelo: ollama pull llama3.2:3b")
        return
    
    print()
    
    # Verificar modelos
    models = check_available_models()
    if not models:
        print("\nPara descargar un modelo:")
        print("   ollama pull llama3.2:3b  # Modelo pequeño y rápido")
        print("   ollama pull llama3        # Modelo completo")
        return
    
    print()
    
    # Probar consulta
    working_model = test_model_query()
    if working_model:
        print(f"\nTodo listo! Modelo recomendado: {working_model}")
    else:
        print("\nLos modelos están instalados pero no responden correctamente")

if __name__ == "__main__":
    main()