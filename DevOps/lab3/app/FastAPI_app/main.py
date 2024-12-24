from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


users = []


@app.get("/")
async def root():
    return {"message": "root directory"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/users")
async def add_users(user: User):
    users.append(user)
    return {"message": f"User {user.name} added."}


@app.get("/users/")
async def list_users(limit: int = 10):
    return users[0:limit]


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id < len(users):
        user = users[user_id]
        return {"message": f"name:('{user.name}', {user.age})"}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

