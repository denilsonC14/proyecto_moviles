from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .documento import Documento


@dataclass
class Consulta:
    """Entidad de dominio que representa una consulta de búsqueda."""
    
    pregunta: str
    limite_resultados: int = 5
    fecha_consulta: Optional[datetime] = None
    
    def __post_init__(self):
        if self.fecha_consulta is None:
            self.fecha_consulta = datetime.now()
    
    def es_valida(self) -> bool:
        """Valida si la consulta tiene los parámetros mínimos."""
        return (
            bool(self.pregunta.strip()) and 
            self.limite_resultados > 0 and 
            self.limite_resultados <= 20
        )


@dataclass
class ResultadoConsulta:
    """Entidad que representa el resultado de una consulta."""
    
    respuesta_ia: str
    documentos_relevantes: List[Documento]
    consulta_original: str
    tiempo_procesamiento: Optional[float] = None
    
    @property
    def tiene_documentos_relevantes(self) -> bool:
        return len(self.documentos_relevantes) > 0
    
    @property
    def numero_documentos(self) -> int:
        return len(self.documentos_relevantes)


@dataclass
class Usuario:
    """Entidad de dominio que representa un usuario del sistema."""
    
    id: int
    username: str
    hashed_password: str
    fecha_registro: Optional[datetime] = None
    
    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()
    
    def es_valido(self) -> bool:
        """Valida si el usuario tiene los campos mínimos."""
        return (
            bool(self.username.strip()) and 
            len(self.username.strip()) >= 3 and
            bool(self.hashed_password)
        )