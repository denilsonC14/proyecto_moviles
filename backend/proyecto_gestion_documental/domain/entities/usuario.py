from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Usuario:
    username: str
    hashed_password: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()