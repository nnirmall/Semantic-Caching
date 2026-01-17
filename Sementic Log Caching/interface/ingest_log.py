from typing import Optional
from pydantic import BaseModel

class IngestLog(BaseModel):
    status: str
    action: str
    id: str
    source: Optional[str] = None

    