from  fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello_check():
    return {
        "msg":"despliegue prod version 1"
    }

if __name__ == "__main__":
    uvicorn.run(
        "entrypoint:app",
        host="0.0.0.0",
        port=5000
    )
