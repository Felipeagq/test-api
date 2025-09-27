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

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    posts = relationship("PostModel", back_populates="owner")

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="posts")

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    name: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str

app = FastAPI(
    title="Servidor en clase",
    version="0.0.1",
    description="Descripción de servidor"
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


def require_roles(*roles):
    def role_checker(user: UserModel = Depends(get_current_user)):
        user_roles_names = user.role
        if not any(r in user_roles_names for r in roles):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker




@app.get("/")
def hello_check():
    return {
        "msg":"ok"
    }

@app.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
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

@app.get("/users/{user_id}")
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

@app.get("/list")
def users_lists( db: Session = Depends(get_db),current_user: UserModel = Depends(require_roles("admin"))):
    user = db.query(UserModel).all()
    return user


@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_roles("admin","user"))):
    new_post = PostModel(
        title=post.title, # titulo al post
        content=post.content,  # contenido al post
        user_id=current_user.id # al usuario loggeado
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
@app.get("/posts/")
def get_my_posts(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(PostModel).filter_by(user_id=current_user.id).all()


@app.get("/protected/admin-area")
def admin_area(current_user: UserModel = Depends(require_roles("admin"))):
    return {
        "msg": "Welcome to the admin area",
        "data":current_user
    }

@app.get("/protected/admin-user-area")
def admin_user_area(current_user: UserModel = Depends(require_roles("admin","user"))):
    return {
        "msg": "Welcome to the admin user area",
        "data":current_user
        }

@app.get("/protected/user-area")
def user_area(current_user: UserModel = Depends(require_roles("user"))):
    return {
        "msg": "Welcome to the user area",
        "data":current_user
        }



if __name__ == "__main__":
    uvicorn.run(
        "entrypoint:app",
        host="localhost",
        port=8085,
        reload=True
    )
