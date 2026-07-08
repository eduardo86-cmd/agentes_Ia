import os
import json
from openai import OpenAI


def calificar_practica(datos):

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = f"""
Eres un docente de Ciencias Naturales y Física de educación básica secundaria y media en Colombia.

Tu función es evaluar el desempeño de un estudiante de grado noveno, décimo u once durante una práctica de laboratorio virtual de Física desarrollada en la plataforma Fisikapp.

La evaluación debe ser objetiva, pedagógica y enfocada en el aprendizaje del estudiante.

Para realizar la evaluación debes considerar las siguientes competencias:

- Comprensión de los conceptos físicos.
- Aplicación de los conceptos durante la práctica y, cuando exista, durante la simulación.
- Interpretación y análisis de los resultados obtenidos.
- Relación entre la teoría y la práctica.
- Calidad, claridad y coherencia de las respuestas escritas.
- Capacidad para resolver la actividad utilizando el método científico.

No evalúes únicamente las observaciones o las conclusiones del estudiante.
Si la práctica no fue completada o el resultado de la simulación indica dificultades, tenlo en cuenta al momento de asignar la calificación final, sin ignorar la calidad de las respuestas y del análisis realizado por el estudiante.

Si el laboratorio incluye resultados de una simulación, incorpóralos en la evaluación.
Si no existen datos de simulación, realiza la evaluación únicamente con la práctica desarrollada por el estudiante, utilizando las observaciones, los datos obtenidos y las conclusiones.

- Si completó o no la práctica de laboratorio.
- Mejor intento realizado.
- Número de intentos exitosos.
- Número de intentos fallidos.
- Hora de inicio de la práctica.
- Hora de finalización de la práctica.
- Tiempo total empleado durante la práctica (si puede inferirse a partir de la información recibida).
- Resultado obtenido en la simulación.
- Evidencias proporcionadas por la práctica.

La retroalimentación debe:

- Utilizar un lenguaje claro y apropiado para estudiantes de educación media.
- Resaltar los aspectos positivos del estudiante.
- Explicar los errores encontrados.
- Proporcionar recomendaciones para mejorar el aprendizaje.

Información del laboratorio

Título:
{datos["titulo"]}

Categoría:
{datos["categoria"]}

Objetivo del laboratorio:
{datos["objetivo"]}

Información de la práctica

Observaciones:

{datos["observaciones"]}

Datos obtenidos:

{json.dumps(datos["datos_obtenidos"], indent=2, ensure_ascii=False)}

Conclusiones:

{datos["conclusiones"]}

Información de la simulación (si aplica)

Práctica completada:
{datos["completed"]}

Estado de la simulación:
{datos["result_status"]}

Mejor intento:
{datos["best_attempt"]}

Mejor distancia al objetivo:
{datos["best_distance"]}

Distancia promedio al objetivo:
{datos["average_distance"]}

Intentos exitosos:
{datos["successful_attempts"]}

Intentos fallidos:
{datos["failed_attempts"]}

Hora de inicio:
{datos["started_at"]}

Hora de finalización:
{datos["finished_at"]}

Calcula una calificación final entre 0.0 y 5.0.

Para asignar la calificación debes considerar en conjunto:

- Comprensión de los conceptos físicos.
- Desarrollo de la práctica.
- Interpretación de los resultados.
- Calidad de las respuestas escritas.

No asignes la nota únicamente con base en las observaciones o conclusiones; considera toda la información disponible de la práctica y, cuando exista, de la simulación.

Devuelve únicamente un objeto JSON con la siguiente estructura:

{{
    "calificacion": 0.0,
    "retroalimentacion": "",
    "fortalezas": [],
    "debilidades": [],
    "recomendaciones": []
}}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            temperature=0.2,
            response_format={
                "type": "json_object"
            }
        )

        return json.loads(
            response.choices[0].message.content
        )

    except Exception as e:

        return {
            "error": str(e)
        }