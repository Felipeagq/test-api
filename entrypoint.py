
from fastapi import FastAPI

app = FastAPI()

# Lista simple para guardar datos
datos = []

# GET: Ver todos los datos
@app.get("/")
def ver_datos():
    return datos

# POST: Agregar un dato
@app.post("/")
def agregar_dato(dato: dict):
    datos.append(dato)
    return {"mensaje": "Dato agregado"}

# PUT: Reemplazar un dato por su posición
@app.put("/{posicion}")
def actualizar_dato(posicion: int, nuevo_dato: dict):
    datos[posicion] = nuevo_dato
    return {"mensaje": "Dato actualizado"}

# DELETE: Eliminar un dato por su posición
@app.delete("/{posicion}")
def eliminar_dato(posicion: int):
    datos.pop(posicion)
    return {"mensaje": "Dato eliminado"}