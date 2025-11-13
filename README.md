🚀 Basic FastAPI Setup

This repository provides a minimal FastAPI backend setup with SQLAlchemy integration — ideal for beginners who want to understand how to create, read, update, and delete (CRUD) data using FastAPI and a relational database.

📋 Prerequisites

Before you begin, ensure that you have the following installed:

Python 3.8+

pip (Python package manager)

Virtual environment (recommended)

⚙️ Installation
1. Clone the Repository
git clone https://github.com/your-username/basic_fastapi_setup.git
cd basic_fastapi_setup

2. Create and Activate Virtual Environment
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install fastapi[all]
pip install sqlalchemy


Alternatively, you can install everything at once:

pip install -r requirements.txt

📁 Project Structure
basic_fastapi_setup/
│
├── main.py                 # Entry point of the application
├── models.py               # SQLAlchemy database models
├── database.py             # Database connection setup
├── schemas.py              # Pydantic schemas for request/response validation
├── crud.py                 # CRUD operation functions
└── README.md               # Project documentation

🚀 Running the Application

Run the FastAPI development server using Uvicorn:

uvicorn main:app --reload

Open your browser:

API docs (Swagger UI): 👉 http://127.0.0.1:8000/docs

Alternative ReDoc docs: 👉 http://127.0.0.1:8000/redoc

🧩 Example Code Overview
main.py
from fastapi import FastAPI
from database import engine, Base
from models import User

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

models.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

🧠 Next Steps

Once you have this setup working, you can extend it by adding:

🔐 Authentication using JWT

🗂️ Alembic for database migrations

🐳 Docker for containerized deployment

⚡ Async SQLAlchemy for high-performance apps

🧩 PonyORM or Tortoise ORM for alternative ORM experiences

🧾 License

This project is licensed under the MIT License — feel free to use and modify for your learning and projects.
