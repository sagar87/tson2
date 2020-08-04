from app.api.models import NoteSchema
from app.db import sample, types, variant, count, notes, dataset, database
from app.api.types import SNV
import pandas as pd
from io import StringIO

async def post(payload: NoteSchema):
    query = notes.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(id: int):
    # query = notes.select().where(id == notes.c.id)
    q = "SELECT * FROM notes WHERE id = :id"
    return await database.fetch_one(query=q, values={"id": id})

async def get_all():
    q = "SELECT * FROM notes"
    return await database.fetch_all(query=q)

async def put(id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)

async def get_all_variants():
    q = "SELECT * FROM variant"
    return await database.fetch_all(query=q)


async def get_sample(id: int):
    q = """
    SELECT c.value, v.name, v.id 
        FROM count AS c 
            INNER JOIN variant AS v
        ON c.variant_id = v.id 
    WHERE c.sample_id = (:id);"""
    print("GOT", id)
    return await database.fetch_all(query=q, values={"id": id})
    
async def get_dataset(slug: str):
    q = """
    SELECT s.id, s.name AS sample, d.name as dataset 
        FROM sample AS s 
            INNER JOIN dataset AS d 
        ON s.dataset_id = d.id 
    WHERE d.name = (:slug);
    """
    return await database.fetch_all(query=q, values={"slug": slug})

async def create_dataset(file, slug: str, delim: str, sample_dim: str, header: str):
    test = await file.read()
    
    if header == "false": 
        data = pd.read_csv(StringIO(test.decode()), sep=delim, header=None)
    else:
        data = pd.read_csv(StringIO(test.decode()), sep=delim)

    query = dataset.insert().values(name=slug)
    current_dataset = await database.execute(query=query)

    print ("dataset", current_dataset)

    row_num, col_num = data.shape

    if sample_dim == "row":
        data = data.T
    
    print(data)

    for sample_name in data.columns:
        # insert_sample_query = "INSERT INTO sample(name, dataset_id) VALUES (:name, :dataset_id)"
        # insert_sample_value = {"name": str(sample_name), "dataset_id": current_dataset}
        insert_sample_query = sample.insert().values(name=str(sample_name), dataset_id=current_dataset)
        sample_id = await database.execute(query=insert_sample_query)

        insert_counts_query = "INSERT INTO count(value, sample_id, variant_id) VALUES (:value, :sample_id, :variant_id)"
        insert_counts_values = [ {"value": count, "variant_id": variant_id+1, "sample_id": sample_id } for variant_id, count in enumerate(data[sample_name]) ]
        
        sample_id =  await database.execute_many(query=insert_counts_query, values=insert_counts_values)
