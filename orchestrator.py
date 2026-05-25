from agents.input_agent import preparar_entrada
from agents.model_agent import buscar_contexto
from agents.output_agent import (
    formatear_contenido,
    formatear_actividades,
    formatear_detalle
)

def generar_contenido_orquestado(datos):
    datos_limpios = preparar_entrada(datos)
    fila, score = buscar_contexto(datos_limpios["categoria"],datos_limpios["titulo"],
    datos_limpios["objetivo"])
    return formatear_contenido(fila,score)

def generar_actividades_orquestado(datos):
    datos_limpios=preparar_entrada(datos)
    return formatear_actividades(datos_limpios)

def generar_detalle_orquestado(datos):
    datos_limpios =preparar_entrada(datos)
    return formatear_detalle(datos_limpios)