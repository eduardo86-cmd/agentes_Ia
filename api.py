from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    palabras_clave: str

@app.get("/")
def inicio():
    return {"message": "Backend IA Fisikapp funcionando"}

@app.post("/generar-contenido")
def generar_contenido(datos: DatosEntrada):
    resumen = (
        f"Este proyecto pertenece a la categoría de {datos.categoria}. "
        f"Su objetivo principal es {datos.objetivo}. "
        f"Se abordarán conceptos relacionados con {datos.palabras_clave}."
    )

    prologo = (
        f"El presente trabajo se desarrolla en el área de {datos.categoria}, "
        f"con el propósito de fortalecer el análisis y comprensión del tema. "
        f"A partir del objetivo planteado, se busca explicar de manera clara los conceptos asociados a "
        f"{datos.palabras_clave}."
    )

    marco_teorico = (
        f"El marco teórico de este proyecto se fundamenta en la categoría de {datos.categoria}. "
        f"Para cumplir el objetivo de {datos.objetivo}, se consideran conceptos clave como "
        f"{datos.palabras_clave}. Estos elementos permiten comprender las bases del tema, "
        f"su importancia y su aplicación dentro del contexto académico."
    )

    return {
        "resumen": resumen,
        "prologo": prologo,
        "marco_teorico": marco_teorico
    }

