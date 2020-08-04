from app.api import crud
from app.api.models import VariantSchema
from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Form
from typing import List


router = APIRouter()


@router.get("/variant", response_model=List[VariantSchema])
async def get_all():
    return await crud.get_all_variants()

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), slug: str = Form(...), delim: str = Form(...), sample: str = Form(...), header: str = Form(...)):
    await crud.create_dataset(file, slug, delim, sample, header)
    
    return {"filename": file.filename}


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@router.get("/sample/{id}")
async def get_dataset(id: int= Path(..., gt=0)):
    return await crud.get_sample(id)
    

@router.get("/dataset/{slug}")
async def get_dataset(slug: str):
    return await crud.get_dataset(slug)
    



