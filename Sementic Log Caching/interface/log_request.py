from typing import Any, Dict
from pydantic import BaseModel


class LogRequest(BaseModel):
    source: str
    payload: Dict[str, Any]