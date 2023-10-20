from  fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello_check():
    return {
        "msg":"Hola mundo"
    }

if __name__ == "__main__":
    uvicorn.run(
        "entrypoint:app",
    )