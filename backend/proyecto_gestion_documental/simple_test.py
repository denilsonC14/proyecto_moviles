#!/usr/bin/env python3
"""Prueba simple de la API"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("=== PRUEBA DE API ===")
    
    # Test 1: Estado
    print("1. Probando estado...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("[OK] API funcionando")
        else:
            print(f"[ERROR] API error: {response.status_code}")
            return
    except:
        print("[ERROR] No se puede conectar a la API")
        return
    
    # Test 2: Subir documento
    print("2. Subiendo documento...")
    doc = {
        "titulo": "Manual de Procedimientos",
        "contenido": "Los empleados deben reportar cualquier incidente de seguridad inmediatamente. El proceso incluye: 1) Notificar al supervisor, 2) Llenar el formulario de incidentes, 3) Seguir las medidas correctivas.",
        "tipo": "normativo"
    }
    
    try:
        response = requests.post(f"{base_url}/documentos/", json=doc)
        if response.status_code == 200:
            print("[OK] Documento subido")
        else:
            print(f"[ERROR] Error subiendo: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 3: Listar documentos
    print("3. Listando documentos...")
    try:
        response = requests.get(f"{base_url}/documentos/")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] {data['total']} documentos encontrados")
        else:
            print(f"[ERROR] Error listando: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 4: Consulta RAG
    print("4. Probando consulta RAG...")
    consulta = {
        "pregunta": "Como debo reportar un incidente de seguridad?",
        "limite_resultados": 3
    }
    
    try:
        response = requests.post(f"{base_url}/consultas/", json=consulta)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Consulta procesada")
            print(f"Respuesta: {data['respuesta_ia'][:150]}...")
            print(f"Documentos relevantes: {len(data['documentos_relevantes'])}")
        else:
            print(f"[ERROR] Error en consulta: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    test_api()