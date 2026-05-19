from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import unicodedata
from rapidfuzz import fuzz

def limpiar_texto(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.strip()

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
    mejor_score = 0

    categoria_usuario = limpiar_texto(datos.categoria)

    for _, fila in df.iterrows():
        categoria_csv = limpiar_texto(fila["categoria"])

        score = fuzz.ratio(categoria_usuario, categoria_csv)

        if score > mejor_score:
            mejor_score = score
            fila_encontrada = fila

    if mejor_score < 60:
        fila_encontrada = None

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
        "marco_teorico": marco_teorico,
        "coincidencia": mejor_score
    }