# 🚀 Basic FastAPI Setup

This repository provides a **minimal FastAPI backend** setup with **SQLAlchemy** integration — ideal for beginners who want to understand how to create, read, update, and delete (CRUD) data using FastAPI and a relational database.

---

## 📋 Prerequisites

Before you begin, ensure that you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Virtual environment** (recommended)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/basic_fastapi_setup.git
cd basic_fastapi_setup
```

### 2. Create and Activate Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install fastapi[all]
pip install sqlalchemy
```

Alternatively, you can install everything at once:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
basic_fastapi_setup/
│
├── main.py                 # Entry point of the application
├── models.py               # SQLAlchemy database models
├── database.py             # Database connection setup
├── schemas.py              # Pydantic schemas for request/response validation
├── crud.py                 # CRUD operation functions
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Running the Application

Run the FastAPI development server using Uvicorn:

```bash
uvicorn main:app --reload
```

Open your browser:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc UI**: http://127.0.0.1:8000/redoc

---

## 🧩 Example Code Overview

### main.py

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from schemas import UserCreate, UserResponse
import crud

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

### database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### models.py

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

### schemas.py

```python
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
```

### crud.py

```python
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
```

### requirements.txt

```
fastapi[all]
sqlalchemy
uvicorn[standard]
```

---

## 🧠 Next Steps

Once you have this setup working, you can extend it by adding:

- 🔐 **JWT Authentication** for user login and security
- 🗂️ **Alembic** for database migrations
- 🐳 **Docker** for containerized deployment
- ⚡ **Async SQLAlchemy** for improved performance
- 🧩 **PonyORM** or **Tortoise ORM** as alternatives to SQLAlchemy
- 🧪 **Pytest** for testing your API endpoints

---

## 🔄 Alternative: Using PonyORM Instead of SQLAlchemy

If you prefer **PonyORM** for its more pythonic syntax and automatic query optimization, here's how to adapt the setup:

### Installation

```bash
pip install pony
```

### database.py (PonyORM version)

```python
from pony.orm import Database, db_session

db = Database()

def init_db():
    db.bind(provider='sqlite', filename='test.db', create_db=True)
    db.generate_mapping(create_tables=True)
```

### models.py (PonyORM version)

```python
from pony.orm import PrimaryKey, Required
from database import db

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    email = Required(str, unique=True)
```

### main.py (PonyORM version)

```python
from fastapi import FastAPI, HTTPException
from pony.orm import db_session, select
from database import db, init_db
from models import User
from schemas import UserCreate, UserResponse

app = FastAPI()

# Initialize database
init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PonyORM!"}

@app.post("/users/", response_model=UserResponse)
@db_session
def create_user(user: UserCreate):
    new_user = User(name=user.name, email=user.email)
    return new_user.to_dict()

@app.get("/users/", response_model=list[UserResponse])
@db_session
def read_users():
    users = select(u for u in User)[:]
    return [u.to_dict() for u in users]
```

### Key Differences

- **PonyORM** uses decorators like `@db_session` instead of dependency injection
- Models inherit from `db.Entity` instead of `Base`
- Queries use pythonic generator expressions: `select(u for u in User)`
- No need for explicit `commit()` — changes auto-commit at end of `@db_session`

---

## 🧾 License

This project is licensed under the MIT License — feel free to use, modify, and distribute for your learning and projects.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

**Happy Coding! 🎉**
