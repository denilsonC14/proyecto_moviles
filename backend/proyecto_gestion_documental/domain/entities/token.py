from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Token:
    access_token: str
    token_type: str = "bearer"
    expires_at: Optional[datetime] = None
    user_id: Optional[int] = None
    
    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)
    
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at