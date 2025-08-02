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
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str

# class User(BaseModel):
#     username: str
#     name: str
#     email: str

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

@app.post("/register",
        #   response_model=User
          )
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=user.username).first():
        return {"message":"usuario ya existe, verificar"}
    data = user.model_dump()
    data["password"] = hash_password(data["password"])
    new_user = UserModel(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(username=form_data.username).first()
    if not user or user.password != hash_password(form_data.password):
        return {"message":"Credenciales invalidas"}
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/{user_id}"
        #  ,response_model=User
         ) # se usa response model para modificar la salida
def me(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    return user

@app.delete("/users/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado",
            "user":user}

@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_post = PostModel(title=post.title, content=post.content, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/")
def get_my_posts(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(PostModel).filter_by(user_id=current_user.id).all()

if __name__ == "__main__":
    uvicorn.run("paso_7:app",
                host="localhost",
                port=8080,
                reload=True)
