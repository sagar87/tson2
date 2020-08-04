from pydantic import BaseModel, Field
from fastapi import UploadFile, File





class VariantSchema(BaseModel):
    name: str = Field(..., max_length=16)
    type_id: str

class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int