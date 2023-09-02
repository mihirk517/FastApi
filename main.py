from fastapi import FastAPI, status,APIRouter
from fastapi.params import Body
from typing import Optional,List
#from random import randrange
import app.routers.posts as posts,app.routers.users as users,app.routers.auth as auth,app.routers.vote as vote
from psycopg2.extras import RealDictCursor
import time ,psycopg2
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.config import Settings
from app import models


router  = APIRouter()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#while True:
#    try:
#        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin",
#                                cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("Connected to Database")
#        break
#    except Exception as e:
#        print(f"Connection Error {e.args}")
#        time.sleep(2)

my_posts = [{"title": "title of post1", "content": "content of post1", "id": 1},
            {"title": "Photos", "content": "Photos to be printed", "id": 2}]


def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", status_code=status.HTTP_201_CREATED)
async def root():
    return {"message": "Welcome"}




