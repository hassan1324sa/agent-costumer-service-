from pydantic import BaseModel

class RetrieveDocs(BaseModel):
    dataId: str
    question: str
    answer: str
    score: float | None = None
