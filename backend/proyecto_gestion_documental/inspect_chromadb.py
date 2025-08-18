import chromadb

# Inicializar el cliente de ChromaDB
chroma_client = chromadb.Client()

# Acceder a la colección (asegúrate que el nombre coincide)
collection = chroma_client.get_collection(name="documentos_normativos")

# Obtener todos los documentos almacenados
resultados = collection.get()

# Mostrar información relevante
print("IDs:", resultados.get("ids"))
print("Metadatos:", resultados.get("metadatas"))
print("Documentos:", resultados.get("documents"))
print("Embeddings:", resultados.get("embeddings"))
