from agents.input_agent import preparar_entrada
from agents.model_agent import buscar_contexto
from agents.groq_agent import (generar_detalle_con_groq, generar_actividades_con_groq,generar_contenido_con_groq)
from agents.output_agent import (
    formatear_contenido,
    formatear_actividades
)

def generar_contenido_orquestado(datos):
    datos_limpios = preparar_entrada(datos)

    fila, score = buscar_contexto(
        datos_limpios["categoria"],
        datos_limpios["titulo"],
        datos_limpios["objetivo"]
    )

    if fila is None:
        return {
            "error": "No se encontró contexto suficiente en el dataset."
        }

    contexto = {
        "resumen": fila.get("resumen", ""),
        "introduccion": fila.get("introduccion", ""),
        "marco_teorico": fila.get("marco_teorico", "")
    }

    return generar_contenido_con_groq(datos_limpios, contexto)

def generar_actividades_orquestado(datos):
    datos_limpios = preparar_entrada(datos)

    fila, score = buscar_contexto(
        datos_limpios["categoria"],
        datos_limpios["titulo"],
        datos_limpios["objetivo"]
    )

    if fila is None:
        return {
            "error": "No se encontró contexto suficiente en el dataset."
        }

    contexto = {
        "resumen": fila.get("resumen", ""),
        "introduccion": fila.get("introduccion", ""),
        "marco_teorico": fila.get("marco_teorico", "")
    }

    return generar_actividades_con_groq(datos_limpios, contexto)

def generar_detalle_orquestado(datos):
    datos_limpios = preparar_entrada(datos)

    fila, score = buscar_contexto(
        datos_limpios["categoria"],
        datos_limpios["titulo"],
        datos_limpios["objetivo"]
    )

    if fila is None:
        return {
            "error": "No se encontró contexto suficiente en el dataset."
        }

    contexto = {
        "resumen": fila.get("resumen", ""),
        "introduccion": fila.get("introduccion", ""),
        "marco_teorico": fila.get("marco_teorico", "")
    }

    return generar_detalle_con_groq(datos_limpios, contexto)

