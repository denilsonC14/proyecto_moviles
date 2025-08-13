#!/usr/bin/env python3
"""Script para probar la API de Gestión Documental"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_status():
    """Prueba el endpoint de estado de la API"""
    print("🔍 Probando estado de la API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error en API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. ¿Está corriendo el servidor?")
        return False

def test_upload_document():
    """Prueba subir un documento de prueba"""
    print("\n📄 Probando subida de documento...")
    
    documento_prueba = {
        "titulo": "Reglamento de Seguridad Laboral",
        "contenido": """
        ARTÍCULO 1. Todo trabajador debe usar equipos de protección personal (EPP) 
        durante su jornada laboral. Los EPP incluyen casco, guantes de seguridad, 
        calzado de seguridad y chaleco reflectivo.
        
        ARTÍCULO 2. Se prohíbe fumar en todas las áreas de trabajo. Las áreas 
        designadas para fumar están claramente señalizadas.
        
        ARTÍCULO 3. En caso de emergencia, todo el personal debe dirigirse 
        inmediatamente a los puntos de encuentro establecidos siguiendo las 
        rutas de evacuación señalizadas.
        """,
        "tipo": "normativo"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/documentos/", json=documento_prueba)
        if response.status_code == 200:
            print("✅ Documento subido exitosamente")
            print(f"   ID del documento: {response.json()['id']}")
            return True
        else:
            print(f"❌ Error subiendo documento: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_list_documents():
    """Prueba listar documentos"""
    print("\n📋 Probando listado de documentos...")
    
    try:
        response = requests.get(f"{BASE_URL}/documentos/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Se encontraron {data['total']} documentos")
            for doc in data['documentos']:
                print(f"   - {doc['titulo']} (ID: {doc['id']})")
            return True
        else:
            print(f"❌ Error listando documentos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_query_documents():
    """Prueba hacer una consulta"""
    print("\n🤖 Probando consulta con RAG...")
    
    consulta = {
        "pregunta": "¿Qué equipos de protección debo usar en el trabajo?",
        "limite_resultados": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/consultas/", json=consulta)
        if response.status_code == 200:
            data = response.json()
            print("✅ Consulta procesada exitosamente")
            print(f"   Respuesta IA: {data['respuesta_ia'][:200]}...")
            print(f"   Documentos relevantes: {len(data['documentos_relevantes'])}")
            return True
        else:
            print(f"❌ Error en consulta: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la API...")
    print("=" * 50)
    
    # Prueba 1: Estado de la API
    if not test_api_status():
        print("\n❌ La API no está funcionando. Inicia el servidor con: python main.py")
        return
    
    # Prueba 2: Subir documento
    if not test_upload_document():
        print("\n❌ Falla en subida de documentos")
        return
    
    # Dar tiempo para que se procese el embedding
    print("\n⏳ Esperando procesamiento de embeddings...")
    time.sleep(2)
    
    # Prueba 3: Listar documentos
    if not test_list_documents():
        print("\n❌ Falla en listado de documentos")
        return
    
    # Prueba 4: Consulta RAG (solo si Ollama está disponible)
    print("\n⚠️  Nota: La consulta RAG requiere Ollama corriendo en localhost:11434")
    test_query_documents()
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    main()