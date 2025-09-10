from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    created_at: datetime
    due: Optional[datetime] = None
    tags: List[str] = []
    list: Optional[str] = None
    done: bool = False
