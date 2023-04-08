from fastapi import FastAPI, status, HTTPException, Response, Depends
from typing import List, Optional
from random import randrange
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='sorhan', 
                                password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        sleep(2) # wait 2 seconds in case of not connecting db

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def get_user():
    return {"message": "Hello World"}