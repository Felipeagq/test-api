from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import hashlib

# Configuración base de datos
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Modelos SQLAlchemy
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    posts = relationship("PostModel", back_populates="owner")

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="posts")

Base.metadata.create_all(bind=engine)


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

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Helpers

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_id: int) -> str:
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    return user

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
    uvicorn.run("paso_5:app",
                host="localhost",
                port=8080,
                reload=True)
