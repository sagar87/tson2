from app.db import notes, database
from app.api.types import SNV
from app.api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List


router = APIRouter()

@router.get("/types")
async def populate_db():
    query = "INSERT INTO types(name) VALUES (:name)"
    values = [ {"name": "SNV"}, {"name": "MNV"}, {"name": "insertion"}, {"name": "deletion"}, {"name": "SV"}]
    await database.execute_many(query=query, values=values)

@router.get("/snv")
async def populate_snv():
    query = "INSERT INTO variant(name, type_id) VALUES (:name, :type_id)"
    values = [{"name": n, "type_id": 1} for n in SNV]
    await database.execute_many(query=query, values=values)

