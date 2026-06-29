from agents.input_agent import (preparar_entrada,preparar_entrada_evaluacion)
from agents.model_agent import buscar_contexto
from agents.evaluation_agent import calificar_practica
from agents.image_agent import (
    generar_imagen,
    generar_imagen_base64)

from agents.groq_agent import (
    generar_detalle_con_groq,
    generar_actividades_con_groq,
    generar_contenido_con_groq,
    generar_prompt_visual_con_groq,
    generar_prompt_desde_procedimiento,
    filtrar_pasos_visuales,
    generar_prompt_desde_pasos_visuales,
    generar_portada_con_groq,
    generar_prompt_portada,
    
)

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

    detalle = generar_detalle_con_groq(
        datos_limpios,
        contexto
    )

    print("\nDETALLE COMPLETO:\n")
    print(detalle)

    print("\nPROCEDIMIENTO:\n")
    print(detalle.get("procedimiento"))

    return detalle


def generar_imagen_orquestada(datos):
    datos_limpios = preparar_entrada(datos)

    fila, score = buscar_contexto(
        datos_limpios["categoria"],
        datos_limpios["titulo"],
        datos_limpios["objetivo"]
    )

    contexto = {}

    if fila is not None:
        contexto = {
            "resumen": fila.get("resumen", ""),
            "introduccion": fila.get("introduccion", ""),
            "marco_teorico": fila.get("marco_teorico", "")
        }

    detalle = generar_detalle_con_groq(
        datos_limpios,
        contexto
    )

    procedimiento = detalle.get("procedimiento", [])

    pasos_visuales = filtrar_pasos_visuales(
        procedimiento
    )

    prompt_visual = generar_prompt_desde_pasos_visuales(
        datos_limpios,
        pasos_visuales
    )

    prompt_visual = prompt_visual.strip().strip('"')

    print("\nPASOS VISUALES:\n")
    print(pasos_visuales)

    print("\nPROMPT VISUAL DINÁMICO:\n")
    print(prompt_visual)

    print("\n====================\n")

    return generar_imagen(prompt_visual)

def generar_portada_orquestada(datos):
    datos_limpios = preparar_entrada(datos)

    fila, score = buscar_contexto(
        datos_limpios["categoria"],
        datos_limpios["titulo"]
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

    portada = generar_portada_con_groq(
        datos_limpios,
        contexto
    )

    return portada

def generar_imagen_portada_orquestada(datos):
    datos_limpios = preparar_entrada(datos)

    prompt_imagen = generar_prompt_portada(
        datos_limpios
    )

    return generar_imagen_base64(
        prompt_imagen
    )

def calificar_practica_orquestada(datos):

    datos_limpios = preparar_entrada_evaluacion(datos)

    if not datos_limpios["titulo"]:
        return {
            "error": "El laboratorio no tiene título."
        }

    if len(datos_limpios["respuestas"]) == 0:
        return {
            "error": "No se recibieron respuestas del estudiante."
        }

    return calificar_practica(
        datos_limpios
    )