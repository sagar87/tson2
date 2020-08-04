from fastapi import FastAPI

from app.api import ping, notes, populate, data
from app.db import engine, metadata, database
from fastapi.middleware.cors import CORSMiddleware
metadata.create_all(engine)

app = FastAPI()
origins = [
    "http://localhost:3007",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(populate.router, prefix="/populate", tags=["populate"])