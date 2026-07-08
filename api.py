from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import Response
from orchestrator import calificar_practica_orquestada
from typing import Any


from orchestrator import(
    generar_portada_orquestada,
    generar_contenido_orquestado,
    generar_actividades_orquestado,
    generar_detalle_orquestado,
    generar_imagen_orquestada,
    generar_imagen_portada_orquestada,
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
    laboratorio_id: int | None = None
    categoria: str
    objetivo: str = ""
    palabras_clave: str = ""
    titulo: str
    resumen: str = ""
    nivel: str = ""
    descripcion: str = ""

class DatosConLaboratorio(BaseModel):
    laboratorio_id: int
    categoria: str
    objetivo: str = ""
    palabras_clave: str = ""
    titulo: str
    resumen: str = ""
    nivel: str = ""
    descripcion: str = ""

class DatosActividad(BaseModel):
    laboratorio_id: int
    actividad_id: int
    categoria: str
    objetivo: str = ""
    palabras_clave: str = ""
    titulo: str
    resumen: str = ""
    nivel: str = ""
    descripcion: str = ""

class DatosPortada(BaseModel):
    categoria: str
    titulo: str


class DatosEvaluacion(BaseModel):
    laboratorio_id: int
    titulo: str
    categoria: str
    objetivo: str = ""
    estudiante: str = ""

    # Práctica
    observaciones: str = ""
    datos_obtenidos: dict[str, Any] = {}
    conclusiones: str = ""

    # Simulación (opcional)
    completed: bool | None = None
    result_status: str | None = None
    best_attempt: int | None = None
    best_distance: float | None = None
    average_distance: float | None = None
    successful_attempts: int | None = None
    failed_attempts: int | None = None
    started_at: str | None = None
    finished_at: str | None = None

@app.get("/")
def inicio():
    return {"message": "Backend IA Fisikapp funcionando"}

@app.post("/generar-contenido")
def generar_contenido(datos: DatosEntrada):
    return generar_contenido_orquestado(datos.dict())


@app.post("/generar-actividades")
def generar_actividades(datos: DatosConLaboratorio):
    resultado = generar_actividades_orquestado(datos.dict())
    resultado["laboratorio_id"]=datos.laboratorio_id
    return resultado
    

@app.post("/generar-detalle-actividad")
def generar_detalle_actividad(datos: DatosActividad):
    resultado = generar_detalle_orquestado(datos.dict())
    resultado["laboratorio_id"]=datos.laboratorio_id
    resultado["actividad_id"] = datos.actividad_id
    return resultado


@app.post("/generar-imagen")
def generar_imagen_endpoint(datos: DatosActividad):
    imagen = generar_imagen_orquestada(datos.dict())

    return Response(
        content=imagen,
        media_type="image/png"
    )

@app.post("/generar-portada")
def generar_portada(datos: DatosPortada):
    return generar_portada_orquestada(datos.dict())

@app.post("/generar-imagen-portada")
def generar_imagen_portada(datos: DatosPortada):
    return {
        "imagen": generar_imagen_portada_orquestada(
            datos.dict()
        )
    }

@app.post("/calificar-practica")
def calificar_practica(datos: DatosEvaluacion):

    return calificar_practica_orquestada(
        datos.dict()
    )