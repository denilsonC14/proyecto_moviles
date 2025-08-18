from typing import List, Optional
import chromadb
from chromadb.config import Settings
from ...domain.entities.documento import Documento
from ...domain.repositories.documento_repository import DocumentoRepository
from ...domain.services.embedding_service import EmbeddingService


class ChromaDocumentoRepository(DocumentoRepository):
    """Implementación del repositorio de documentos usando ChromaDB."""
    
    def __init__(
        self, 
        embedding_service: EmbeddingService,
        collection_name: str = "documentos_normativos",
        chroma_client: Optional[chromadb.Client] = None
    ):
        self.embedding_service = embedding_service
        self.collection_name = collection_name
        
        # Usar cliente proporcionado o crear uno nuevo
        if chroma_client is not None:
            self.client = chroma_client
        else:
            self.client = chromadb.Client()
            
        # Crear o obtener colección
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)
    
    async def obtener_por_id(self, documento_id: str) -> Optional[Documento]:
        """Obtiene un documento por su ID."""
        try:
            resultado = self.collection.get(
                ids=[documento_id],
                include=['documents', 'metadatas']
            )
            
            if not resultado['ids']:
                return None
            
            return self._convertir_a_documento(
                resultado['ids'][0],
                resultado['documents'][0],
                resultado['metadatas'][0]
            )
            
        except Exception as e:
            raise Exception(f"Error al obtener documento {documento_id}: {str(e)}")
    
    async def obtener_todos(self) -> List[Documento]:
        """Obtiene todos los documentos almacenados."""
        try:
            resultado = self.collection.get(
                include=['documents', 'metadatas']
            )
            
            documentos = []
            for i, doc_id in enumerate(resultado['ids']):
                documento = self._convertir_a_documento(
                    doc_id,
                    resultado['documents'][i],
                    resultado['metadatas'][i]
                )
                documentos.append(documento)
            
            return documentos
            
        except Exception as e:
            raise Exception(f"Error al obtener todos los documentos: {str(e)}")
    
    async def guardar(self, documento: Documento) -> str:
        """Guarda un documento y retorna su ID."""
        try:
            # Generar embedding del contenido
            embedding = await self.embedding_service.generar_embedding(
                documento.contenido
            )
            
            # Preparar metadata
            metadata = {
                "titulo": documento.titulo,
                "tipo": documento.tipo,
                "fecha_creacion": documento.fecha_creacion.isoformat() if documento.fecha_creacion else None
            }
            
            # Guardar en ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[documento.contenido],
                metadatas=[metadata],
                ids=[documento.id]
            )
            
            return documento.id
            
        except Exception as e:
            raise Exception(f"Error al guardar documento: {str(e)}")
    
    async def eliminar(self, documento_id: str) -> bool:
        """Elimina un documento por su ID."""
        try:
            self.collection.delete(ids=[documento_id])
            return True
            
        except Exception as e:
            raise Exception(f"Error al eliminar documento {documento_id}: {str(e)}")
    
    async def buscar_por_similitud(
        self, 
        embedding: List[float], 
        limite: int = 5
    ) -> List[Documento]:
        """Busca documentos similares basándose en un embedding."""
        try:
            resultados = self.collection.query(
                query_embeddings=[embedding],
                n_results=limite,
                include=['documents', 'metadatas', 'distances']
            )
            
            documentos = []
            
            if resultados['ids'] and resultados['ids'][0]:
                for i, doc_id in enumerate(resultados['ids'][0]):
                    # Convertir distancia a similitud (1 - distancia)
                    similitud = 1 - resultados['distances'][0][i] if resultados['distances'] else None
                    
                    documento = self._convertir_a_documento(
                        doc_id,
                        resultados['documents'][0][i],
                        resultados['metadatas'][0][i],
                        similitud
                    )
                    documentos.append(documento)
            
            return documentos
            
        except Exception as e:
            raise Exception(f"Error en búsqueda por similitud: {str(e)}")
    
    async def contar_documentos(self) -> int:
        """Cuenta el número total de documentos."""
        try:
            resultado = self.collection.count()
            return resultado
            
        except Exception as e:
            raise Exception(f"Error al contar documentos: {str(e)}")
    
    def _convertir_a_documento(
        self, 
        doc_id: str, 
        contenido: str, 
        metadata: dict, 
        similitud: Optional[float] = None
    ) -> Documento:
        """Convierte datos de ChromaDB a entidad Documento."""
        from datetime import datetime
        
        fecha_creacion = None
        if metadata.get('fecha_creacion'):
            try:
                fecha_creacion = datetime.fromisoformat(metadata['fecha_creacion'])
            except:
                pass
        
        return Documento(
            id=doc_id,
            titulo=metadata.get('titulo', ''),
            contenido=contenido,
            tipo=metadata.get('tipo', 'normativo'),
            fecha_creacion=fecha_creacion,
            similitud=similitud
        )