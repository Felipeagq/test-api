 fastapi import FastAPI
import json

app = FastAPI()
ARCHIVO = "usuarios.json"

# Funciones básicas de lectura/escritura
def leer():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []

def escribir(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f)

# GET todos los usuarios
@app.get("/usuarios")
def ver_usuarios():
    return leer()

# POST agregar usuario
@app.post("/usuarios")
def agregar_usuario(usuario: dict):
    datos = leer()
    datos.append(usuario)
    escribir(datos)
    return {"mensaje": "Usuario agregado"}

# PUT actualizar usuario por índice
@app.put("/usuarios/{i}")
def actualizar_usuario(i: int, usuario: dict):
    datos = leer()
    datos[i] = usuario
    escribir(datos)
    return {"mensaje": "Usuario actualizado"}

# DELETE eliminar usuario por índice
@app.delete("/usuarios/{i}")
def eliminar_usuario(i: int):
    datos = leer()
    eliminado = datos.pop(i)
    escribir(datos)
    return {"mensaje": "Usuario eliminado", "usuario": eliminado}