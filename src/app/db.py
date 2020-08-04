import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, ForeignKey,
                        create_engine)
from sqlalchemy.sql import func

from databases import Database
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# these are SNVs, deletions, insertions etc. 
types = Table('types', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(16), nullable=False),
)

# these are actual types
variant = Table('variant', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(16), nullable=False),
    Column('type_id', Integer, ForeignKey("types.id"), nullable=False),
)


dataset = Table('dataset', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
)

sample = Table('sample', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(256), nullable=False),
    Column('dataset_id', Integer, ForeignKey("dataset.id"), nullable=False),
)

count = Table('count', metadata,
    Column('id', Integer, primary_key=True),
    Column('value', Integer, nullable=False),
    Column('sample_id', Integer, ForeignKey("sample.id"), nullable=False),
    Column('variant_id', Integer, ForeignKey("variant.id"), nullable=False), 
)



# databases query builder
database = Database(DATABASE_URL)