from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn



# Pydantic models
# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str

class PostCreate(BaseModel):
    title: str
    content: str



app = FastAPI(
    title="Blog FastAPI",
    description="API para gestión de blog con FastAPI en python",
    version="v0.0.1"
)

@app.get("/")
def hello_check():
    return {
        "message": "ok"
    }

@app.post("/register")
def register(user: UserCreate):
    return {
        "message": "crear usuario"
    }

@app.post("/login")
def login():
    return {
        "message": "hacer login"
    }

@app.get("/users/{user_id}")
def me(user_id:int):
    return {
        "message": "obtener usuario"
    }

@app.delete("/users/{user_id}")
def delete_user_by_id(user_id:int):
    return {
        "message": "eliminar usuario"
    }

@app.post("/posts/")
def create_post(post:PostCreate):
    return {
        "message": "crear post"
    }
    
@app.get("/posts/")
def get_my_posts():
    return {
        "message": "obtener post"
    }

if __name__ == "__main__":
    uvicorn.run("paso_3:app",
                host="localhost",
                port=8080,
                reload=True)
