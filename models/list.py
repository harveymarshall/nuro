from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class List(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: datetime
    tags: List[str] = []
    tasks: List[str] = []
