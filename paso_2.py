from fastapi import FastAPI
import uvicorn

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
def register():
    return {
        "message": "ok"
    }

@app.post("/login")
def login():
    return {
        "message": "ok"
    }

@app.get("/users/{user_id}")
def me():
    return {
        "message": "ok"
    }

@app.delete("/users/{user_id}")
def delete_user_by_id():
    return {
        "message": "ok"
    }

@app.post("/posts/")
def create_post():
    return {
        "message": "ok"
    }
    
@app.get("/posts/")
def get_my_posts():
    return {
        "message": "ok"
    }

if __name__ == "__main__":
    uvicorn.run("paso_2:app",
                host="localhost",
                port=8080,
                reload=True)
