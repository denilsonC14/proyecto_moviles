#!/usr/bin/env python3
"""Script para subir documentos normativos múltiples o desde JSON"""

import requests
import json
import os
import time

def test_api_connection():
    """Verifica que la API esté funcionando"""
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            return True, base_url
        else:
            print(f"❌ API error: {response.status_code}")
            return False, None
    except:
        print("❌ No se puede conectar a la API")
        print("💡 Asegúrate de que el servidor esté corriendo: python start_server.py")
        return False, None

def subir_documento_individual(base_url, documento, numero=None, total=None):
    """Sube un documento individual"""
    try:
        response = requests.post(
            f"{base_url}/documentos/",
            json=documento,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            doc_id = result.get('id', 'N/A')
            titulo_corto = documento['titulo'][:50] + "..." if len(documento['titulo']) > 50 else documento['titulo']
            
            if numero and total:
                print(f"✅ [{numero:2d}/{total}] {titulo_corto} (ID: {doc_id})")
            else:
                print(f"✅ {titulo_corto} (ID: {doc_id})")
            return True, doc_id
        else:
            print(f"❌ Error {response.status_code}: {documento['titulo'][:50]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Error subiendo '{documento['titulo'][:30]}...': {e}")
        return False, None

def subir_documentos_hardcodeados(base_url):
    """Sube documentos normativos predefinidos"""
    documentos_normativos = [
        {
            "titulo": "Resolución N. 157/2012",
            "contenido": "Aprobar las nuevas ediciones de las Regulaciones Técnicas de Aviación Civil, armonizadas en base a los Reglamentos Aeronáutico Latinoamericanos:\n\nRDAC Parte 061 \"Licencias para Pilotos y sus Habilitaciones\"",
            "tipo": "normativo"
        },
        {
            "titulo": "REGLAMENTO DE LA LEY DE VENTAS DE BIENES POR SORTEO",
            "contenido": "Art. 1.- Toda persona natural o jurídica, para realizar la venta de bienes muebles, inmuebles, objetos o enseres, empleando sistemas de sorteos mediante venta de acciones, contratos o boletos, que no constituyan rifas o sorteos legalmente prohibidos, a más de presentar la documentación que se exige en el Art. 3 de la Ley, si el promotor fuere un particular, deberá determinar sus nombres, cédula de ciudadanía, domicilio, habitación, ocupación y justificar ante la autoridad competente su solvencia moral y económica.",
            "tipo": "normativo"
        },
        {
            "titulo": "MINISTERIO INTERIOR AUTORIZACION DE RIFAS Y SORTEOS",
            "contenido": "Art. 1.- El Ministerio del Interior a través del Organo que designe el Ministro del Interior, continuará ejerciendo las atribuciones relacionadas con la autorización de rifas y sorteos tanto a nivel nacional como en la Provincia de Pichincha.",
            "tipo": "normativo"
        },
        {
            "titulo": "LEY DE VENTAS POR SORTEO",
            "contenido": "Art. 1.- Toda persona natural o jurídica para realizar la venta de bienes muebles, inmuebles, objetos o enseres, empleando sistemas de sorteos mediante venta de acciones, contratos o boletos y siempre que no constituyan rifas o sorteos prohibidos por la ley, está obligado a solicitar por escrito al Subsecretario de Gobierno en Quito, a los gobernadores en provincias, el permiso correspondiente para iniciar la promoción.",
            "tipo": "normativo"
        },
        {
            "titulo": "Ley del Sistema Ecuatoriano de la Calidad",
            "contenido": "Las infracciones determinadas en la presente Ley, serán sancionadas conforme lo siguiente: Sin perjuicio de la sanción penal correspondiente, la fabricación, importación, venta, transporte, instalación o utilización de productos, aparatos o elementos sujetos a reglamentación técnica sin cumplir la misma, cuando tal incumplimiento comporte peligro o daño grave a la seguridad, será sancionada con multa de cinco mil a diez mil dólares.",
            "tipo": "normativo"
        },
        {
            "titulo": "Reglamento de Alojamiento Turístico",
            "contenido": "Art. 7.- Requisitos previo al registro.- Las personas naturales o jurídicas previo a iniciar el proceso de registro del establecimiento de alojamiento turístico, deberán contar con los siguientes documentos: c) Registro Unico de Contribuyentes (RUC), para persona natural o jurídica;",
            "tipo": "normativo"
        },
        {
            "titulo": "Ley de Turismo",
            "contenido": "Art. 5.- Se consideran actividades turísticas las desarrolladas por personas naturales o jurídicas que se dediquen a la prestación remunerada de modo habitual a una o más de las siguientes actividades: a. Alojamiento; b. Servicio de alimentos y bebidas; c. Transportación, cuando se dedica principalmente al turismo; d. Operación; e. La de intermediación, agencia de servicios turísticos y organizadoras de eventos.",
            "tipo": "normativo"
        },
        {
            "titulo": "Ley Orgánica del Sistema Nacional de Contratación Pública",
            "contenido": "Art. 1.- Objeto y Ambito.- Esta Ley establece el Sistema Nacional de Contratación Pública y determina los principios y normas para regular los procedimientos de contratación para la adquisición o arrendamiento de bienes, ejecución de obras y prestación de servicios, incluidos los de consultoría, que realicen los Organismos y dependencias de las Funciones del Estado.",
            "tipo": "normativo"
        },
        {
            "titulo": "Ley de Régimen de Maquila",
            "contenido": "Quien desee acogerse al régimen establecido en esta Ley deberá solicitar previamente al Ministro de Industrias, Comercio, Integración y Pesca, MICIP, la calificación y consiguiente registro como maquiladora.",
            "tipo": "normativo"
        },
        {
            "titulo": "Registro de Empresas de Ensamblaje",
            "contenido": "Establece los requisitos para presentar la solicitud de aprobación de nuevos modelos/versión de CKD, así como los plazos en los que se autorizará o negará el ensamblaje de los modelos/versión correspondientes.",
            "tipo": "normativo"
        }
    ]
    
    print(f"📚 Subiendo {len(documentos_normativos)} documentos normativos predefinidos...")
    print("-" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for i, doc in enumerate(documentos_normativos, 1):
        success, doc_id = subir_documento_individual(base_url, doc, i, len(documentos_normativos))
        
        if success:
            exitosos += 1
        else:
            fallidos += 1
        
        # Pausa pequeña entre documentos
        time.sleep(0.3)
    
    print(f"\n📊 Resultado: ✅ {exitosos} exitosos, ❌ {fallidos} fallidos")
    return exitosos, fallidos

def subir_desde_json(base_url, json_path=None):
    """Sube documentos desde un archivo JSON"""
    if not json_path:
        # Buscar archivo JSON en ubicaciones comunes
        posibles_rutas = [
            r"c:\Users\carlo\Downloads\normativa_transformada_v2.json",
            "normativa_transformada_v2.json",
            "documentos.json",
            "normativa.json"
        ]
        
        json_path = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                json_path = ruta
                break
        
        if not json_path:
            print("❌ No se encontró archivo JSON en las rutas comunes:")
            for ruta in posibles_rutas:
                print(f"   - {ruta}")
            return 0, 0
    
    print(f"📂 Cargando documentos desde: {json_path}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            documentos = json.load(file)
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {json_path}")
        return 0, 0
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON: {e}")
        return 0, 0
    except Exception as e:
        print(f"❌ Error al cargar archivo: {e}")
        return 0, 0
    
    if not documentos:
        print("❌ El archivo JSON está vacío o no tiene documentos válidos")
        return 0, 0
    
    print(f"✅ Cargados {len(documentos)} documentos desde JSON")
    print(f"📤 Iniciando subida...")
    print("-" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for i, doc in enumerate(documentos, 1):
        # Validar estructura del documento
        if not isinstance(doc, dict) or not all(key in doc for key in ['titulo', 'contenido', 'tipo']):
            print(f"❌ [{i:3d}/{len(documentos)}] Documento mal formateado")
            fallidos += 1
            continue
        
        success, doc_id = subir_documento_individual(base_url, doc, i, len(documentos))
        
        if success:
            exitosos += 1
        else:
            fallidos += 1
        
        # Pausa pequeña entre documentos
        time.sleep(0.2)
        
        # Mostrar progreso cada 20 documentos
        if i % 20 == 0:
            print(f"📊 Progreso: {i}/{len(documentos)} ({(i/len(documentos)*100):.1f}%)")
    
    print(f"\n📊 Resultado: ✅ {exitosos} exitosos, ❌ {fallidos} fallidos")
    return exitosos, fallidos

def verificar_documentos(base_url):
    """Verifica los documentos en el sistema"""
    try:
        response = requests.get(f"{base_url}/documentos/")
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"\n📋 Total de documentos en el sistema: {total}")
            
            if data.get('documentos'):
                print("📄 Últimos documentos:")
                for doc in data['documentos'][-5:]:  # Últimos 5
                    titulo_corto = doc['titulo'][:60] + "..." if len(doc['titulo']) > 60 else doc['titulo']
                    print(f"   - {titulo_corto} (ID: {doc['id']})")
        else:
            print(f"❌ Error verificando documentos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en verificación: {e}")

def probar_consulta(base_url):
    """Prueba una consulta RAG"""
    print(f"\n🧪 Probando consulta RAG...")
    
    consulta = {
        "pregunta": "¿Qué requisitos se necesitan para registrar una empresa de turismo?",
        "limite_resultados": 3
    }
    
    try:
        response = requests.post(f"{base_url}/consultas/", json=consulta)
        if response.status_code == 200:
            data = response.json()
            print("✅ Consulta procesada exitosamente")
            print(f"🤖 Respuesta: {data['respuesta_ia'][:200]}...")
            print(f"📄 Documentos relevantes: {len(data['documentos_relevantes'])}")
        else:
            print(f"❌ Error en consulta: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def menu_principal():
    """Menú principal interactivo"""
    print("🏛️  SUBIDA DE DOCUMENTOS NORMATIVOS")
    print("=" * 50)
    
    # Verificar conexión API
    api_ok, base_url = test_api_connection()
    if not api_ok:
        return
    
    while True:
        print(f"\n📋 OPCIONES:")
        print("1. Subir documentos predefinidos (10 documentos)")
        print("2. Subir desde archivo JSON")
        print("3. Verificar documentos en el sistema")
        print("4. Probar consulta RAG")
        print("5. Salir")
        
        opcion = input("\n🔹 Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            print(f"\n📤 Subiendo documentos predefinidos...")
            exitosos, fallidos = subir_documentos_hardcodeados(base_url)
            if exitosos > 0:
                verificar_documentos(base_url)
        
        elif opcion == "2":
            ruta_json = input("📁 Ruta del archivo JSON (Enter para buscar automáticamente): ").strip()
            if not ruta_json:
                ruta_json = None
            exitosos, fallidos = subir_desde_json(base_url, ruta_json)
            if exitosos > 0:
                verificar_documentos(base_url)
        
        elif opcion == "3":
            verificar_documentos(base_url)
        
        elif opcion == "4":
            probar_consulta(base_url)
        
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Selecciona 1-5.")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n⏹️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")