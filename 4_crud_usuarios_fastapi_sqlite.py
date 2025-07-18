from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI()

# Modelo de Usuario
class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    edad: int

# Base de datos SQLite
sqlite_url = "sqlite:///usuarios.db"
engine = create_engine(sqlite_url, echo=False)

# Crear las tablas
SQLModel.metadata.create_all(engine)

# ---------------------- RUTAS FASTAPI ----------------------

# GET: obtener todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():
    with Session(engine) as session:
        usuarios = session.exec(select(Usuario)).all()
        return usuarios

# POST: crear nuevo usuario
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

# PUT: actualizar usuario por ID
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, datos: Usuario):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        usuario.nombre = datos.nombre
        usuario.edad = datos.edad
        session.commit()
        return usuario

# DELETE: eliminar usuario por ID
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        session.delete(usuario)
        session.commit()
        return {"mensaje": "Usuario eliminado"}