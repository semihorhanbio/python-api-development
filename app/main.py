from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

my_posts = [{"title": "title 1", "content": "content 1", "id": 1},
            {"title": "title 2", "content": "content 2", "id": 2}]

@app.get("/")
def get_user():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post,):
    cursor.execute("""
        INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) 
        RETURNING *""", (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} was not found')
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(i)
            break
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            post_dict = post.dict()
            post_dict['id'] = id
            my_posts[i] = post_dict
            break
    
    return {"data": post_dict}