from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from orchestrator import(
    generar_contenido_orquestado,
    generar_actividades_orquestado,
    generar_detalle_orquestado
)



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
    objetivo: str = ""
    palabras_clave: str = ""
    titulo: str
    resumen: str = ""
    nivel: str = ""
    descripcion: str = ""

@app.get("/")
def inicio():
    return {"message": "Backend IA Fisikapp funcionando"}

@app.post("/generar-contenido")
def generar_contenido(datos: DatosEntrada):
    return generar_contenido_orquestado(datos.dict())


@app.post("/generar-actividades")
def generar_actividades(datos: DatosEntrada):
    return generar_actividades_orquestado(datos.dict())

@app.post("/generar-detalle-actividad")
def generar_detalle_actividad(datos: DatosEntrada):
    return generar_detalle_orquestado(datos.dict())