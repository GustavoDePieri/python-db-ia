from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(str):
    """Classe para compatibilidade entre ObjectId do MongoDB e Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return str(v)


class NoteBase(BaseModel):
    """Modelo base para notas."""
    title: str
    content: str
    tags: List[str] = []


class NoteCreate(NoteBase):
    """Modelo para criação de notas."""
    pass


class NoteUpdate(BaseModel):
    """Modelo para atualização de notas."""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class NoteInDB(NoteBase):
    """Modelo de nota como armazenada no banco de dados."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    embedding: Optional[List[float]] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class NoteOut(NoteBase):
    """Modelo para resposta com dados da nota."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True


class SearchQuery(BaseModel):
    """Modelo para consultas de pesquisa."""
    query: str
    limit: int = 5


class AIRequest(BaseModel):
    """Modelo para solicitações de processamento de IA."""
    text: str
    max_tokens: int = 500 