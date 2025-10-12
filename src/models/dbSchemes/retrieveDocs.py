from pydantic import BaseModel
from typing import Optional

class RetrieveDocs(BaseModel):
    dataId: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    score: Optional[float] = None
    text: Optional[str] = None
