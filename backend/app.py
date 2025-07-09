from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from fastapi.middleware.cors import CORSMiddleware


def read_secret(secret_path):
    with open(secret_path, 'r') as f:
        return f.read().strip()


POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PASSWORD = read_secret("/run/secrets/pg_password")


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Numeric)

app = FastAPI()


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "price": float(p.price)} for p in products]
