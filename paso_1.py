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

if __name__ == "__main__":
    uvicorn.run("paso_1:app",
                host="localhost",
                port=8080,
                reload=True)
