from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def get_user():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

@app.post("/createpost")
def create_post(payLoad: dict = Body(...)):
    return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}