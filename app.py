from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

# Post Model


class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get('/')
def read_root():
    return {"welcome": "Welcome to my API"}


@app.get('/posts')
def get_posts():
    return posts


@app.post('/posts')
def save_post(post: Post):
    # print(post.dict())
    # print(type(uuid()))
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]
    # return "received"


@app.get('/posts/{post_id}')
def get_post(post_id: str):
    print(post_id)
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post Not Found")


@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Post Not Found")


@app.put('/posts/{post_id}')
def udpate_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatedPost.title
            posts[index]["content"] = updatedPost.content
            posts[index]["author"] = updatedPost.author
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Post Not Found")
