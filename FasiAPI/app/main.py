from fastapi import FastAPI, Depends

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app import schemas
from app.database import engine, get_db
from typing import List
from routers import posts, users, auth
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.debug = True

# Database connection
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='siri2251105',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successful")
    print("database connection was successful")
except Exception as error:
    print("connection with database has failed")
    print("Error:", error)

# array of posts
my_posts = [{"title": "title 1", "content": "content 1", "id": 1},
            {"title": "kamisama onegai", "content": "tomoe", "id": 2}]


# for retriving tro id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# finding the index for delete operation
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

"""
@app.get("/")
def root():
    return {"message": "My first API"}

@app.get("/machine-details/{machineName}")
def get_machine_details(machineName: str, machine_type: str, thickness: float, operator_name: str):
    voltage = 210
    current = 2.4
    # Perform additional logic or calculations based on the parameters if needed
    return {
        "voltage": voltage,
        "current": current,
        "machine_type": machine_type,
        "welding_thickness": thickness,
        "operator_name": operator_name
    }
"""


@app.get("/getpost")
def post(db: Session = Depends(get_db)):
    # running sql query
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"post_is": posts}


@app.get("/sqlalchemy", response_model=List[schemas.GetPost])
def test(db: Session = Depends(get_db)):
    # select * from posts
    posts = db.query(models.Post).all()

    post_dicts = []
    for post in posts:
        post_dict = post.__dict__
        # Removing internal SQLAlchemy-related attributes
        post_dict.pop("_sa_instance_state", None)
        post_dicts.append(post_dict)

    return post_dicts
