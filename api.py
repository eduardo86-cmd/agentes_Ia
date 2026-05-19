from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

df = pd.read_csv("data/dataset fisikapp.csv")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosEntrada(BaseModel):
    categoria: str
    objetivo: str
    palabras_clave: str = ""
    titulo: str 

@app.get("/")
def inicio():
    return {"message": "Backend IA Fisikapp funcionando"}

@app.post("/generar-contenido")
def generar_contenido(datos: DatosEntrada):

    fila_encontrada = None

    for _, fila in df.iterrows():

        categoria_csv = str(fila["categoria"]).lower()

        if categoria_csv == datos.categoria.lower():
            fila_encontrada = fila
            break

    if fila_encontrada is not None:

        resumen = fila_encontrada["resumen"]
        introduccion = fila_encontrada["introduccion"]
        marco_teorico = fila_encontrada["marco_teorico"]

    else:

        resumen = "No se encontró información."
        introduccion = ""
        marco_teorico = ""

    return {
        "resumen": resumen,
        "introduccion": introduccion,
        "marco_teorico": marco_teorico
    }

