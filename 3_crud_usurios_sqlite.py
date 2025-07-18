from sqlmodel import SQLModel, Field, create_engine, Session, select

# Modelo de Usuario
class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    edad: int

# Conexión a la base de datos SQLite
engine = create_engine("sqlite:///usuarios.db", echo=False)
SQLModel.metadata.create_all(engine)

# Crear usuario
def crear_usuario(nombre: str, edad: int):
    usuario = Usuario(nombre=nombre, edad=edad)
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        print("Usuario agregado.")

# Ver todos los usuarios
def ver_usuarios():
    with Session(engine) as session:
        usuarios = session.exec(select(Usuario)).all()
        for u in usuarios:
            print(f"ID: {u.id}, Nombre: {u.nombre}, Edad: {u.edad}")

# Actualizar usuario
def actualizar_usuario(id: int, nuevo_nombre: str, nueva_edad: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if usuario:
            usuario.nombre = nuevo_nombre
            usuario.edad = nueva_edad
            session.commit()
            print("Usuario actualizado.")
        else:
            print("Usuario no encontrado.")

# Eliminar usuario
def eliminar_usuario(id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if usuario:
            session.delete(usuario)
            session.commit()
            print("Usuario eliminado.")
        else:
            print("Usuario no encontrado.")

# -----------------------
# Ejemplo de uso:
crear_usuario("Ana", 22)
crear_usuario("Luis", 30)
ver_usuarios()

actualizar_usuario(1, "Ana María", 23)
ver_usuarios()

eliminar_usuario(2)
ver_usuarios()