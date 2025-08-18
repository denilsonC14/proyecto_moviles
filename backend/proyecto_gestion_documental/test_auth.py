#!/usr/bin/env python3
"""Script para probar los endpoints de autenticación integrados"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_status():
    """Prueba el endpoint de estado de la API"""
    print("🔍 Probando estado de la API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            data = response.json()
            print(f"   Endpoints disponibles: {list(data.get('endpoints', {}).keys())}")
            return True
        else:
            print(f"❌ Error en API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. ¿Está corriendo el servidor?")
        return False

def test_register():
    """Prueba registro de usuario"""
    print("\n👤 Probando registro de usuario...")
    
    usuario_test = {
        "username": "test_user",
        "password": "test_password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=usuario_test)
        if response.status_code == 200:
            print("✅ Usuario registrado exitosamente")
            data = response.json()
            print(f"   Usuario: {data.get('usuario', {}).get('username')}")
            return True
        elif response.status_code == 400:
            print("⚠️ Usuario ya existe")
            return True  # Está bien si ya existe
        else:
            print(f"❌ Error registrando usuario: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_login():
    """Prueba login de usuario"""
    print("\n🔐 Probando login de usuario...")
    
    usuario_login = {
        "username": "test_user",
        "password": "test_password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=usuario_login)
        if response.status_code == 200:
            print("✅ Login exitoso")
            data = response.json()
            print(f"   Usuario autenticado: {data.get('usuario', {}).get('username')}")
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_login_invalid():
    """Prueba login con credenciales inválidas"""
    print("\n🚫 Probando login con credenciales inválidas...")
    
    usuario_invalid = {
        "username": "test_user",
        "password": "wrong_password"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=usuario_invalid)
        if response.status_code == 401:
            print("✅ Credenciales inválidas rechazadas correctamente")
            return True
        else:
            print(f"❌ Debería rechazar credenciales inválidas, pero retornó: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas de autenticación"""
    print("🚀 Iniciando pruebas de autenticación...")
    print("=" * 50)
    
    # Prueba 1: Estado de la API
    if not test_api_status():
        print("\n❌ La API no está funcionando. Inicia el servidor con: python main.py")
        return
    
    # Prueba 2: Registro
    if not test_register():
        print("\n❌ Falla en registro de usuarios")
        return
    
    # Prueba 3: Login exitoso
    if not test_login():
        print("\n❌ Falla en login de usuarios")
        return
    
    # Prueba 4: Login con credenciales inválidas
    if not test_login_invalid():
        print("\n❌ Falla en validación de credenciales")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Todas las pruebas de autenticación pasaron!")
    print("\n📋 Endpoints disponibles:")
    print("   - POST /register - Registrar usuario")
    print("   - POST /login - Iniciar sesión")
    print("   - GET / - Estado de la API")
    print("   - Documentación: http://localhost:8000/docs")

if __name__ == "__main__":
    main()