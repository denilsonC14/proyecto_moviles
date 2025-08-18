from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Documento:
    """Entidad de dominio que representa un documento normativo."""
    
    id: str
    titulo: str
    contenido: str
    tipo: str
    fecha_creacion: Optional[datetime] = None
    similitud: Optional[float] = None
    
    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()
    
    @property
    def contenido_preview(self) -> str:
        """Retorna una vista previa del contenido limitada a 200 caracteres."""
        if len(self.contenido) <= 200:
            return self.contenido
        return f"{self.contenido[:200]}..."
    
    def es_valido(self) -> bool:
        """Valida si el documento tiene los campos mínimos requeridos."""
        return (
            bool(self.titulo.strip()) and 
            bool(self.contenido.strip()) and 
            bool(self.tipo.strip()) and
            len(self.contenido.strip()) >= 10
        )