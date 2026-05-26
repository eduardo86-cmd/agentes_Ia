import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


def generar_detalle_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico de física para Fisikapp.

Usa únicamente este contexto del dataset:

Resumen:
{contexto.get("resumen", "")}

Introducción:
{contexto.get("introduccion", "")}

Marco teórico:
{contexto.get("marco_teorico", "")}

Actividad:
Título: {datos.get("titulo", "")}
Categoría: {datos.get("categoria", "")}
Objetivo: {datos.get("objetivo", "")}
Nivel: {datos.get("nivel", "")}
Descripción: {datos.get("descripcion", "")}

Genera el detalle de la actividad.

Responde SOLO JSON válido con esta estructura:
{{
  "objetivo_especifico": "",
  "materiales": [],
  "procedimiento": [],
  "formula": "",
  "tiempo_estimado": ""
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Responde solo JSON válido, sin texto adicional."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)


def generar_actividades_con_groq(datos, contexto):

    prompt = f"""
Eres un asistente académico de física para Fisikapp.

Usa SOLO este contexto del dataset:

Resumen:
{contexto.get("resumen", "")}

Introducción:
{contexto.get("introduccion", "")}

Marco teórico:
{contexto.get("marco_teorico", "")}

Datos:
Título: {datos.get("titulo", "")}
Categoría: {datos.get("categoria", "")}
Objetivo: {datos.get("objetivo", "")}

Genera 3 actividades:
- básica
- intermedia
- avanzada

Reglas:
- Deben ser coherentes con el dataset.
- No inventes conceptos fuera del contexto.
- Devuelve SOLO JSON válido.

Formato:

{{
  "actividades": [
    {{
      "nivel": "basico",
      "descripcion": "",
      "resumen": ""
    }},
    {{
      "nivel": "intermedio",
      "descripcion": "",
      "resumen": ""
    }},
    {{
      "nivel": "avanzado",
      "descripcion": "",
      "resumen": ""
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Responde únicamente JSON válido."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    texto = response.choices[0].message.content

    return json.loads(texto)

def generar_contenido_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico de física para Fisikapp.

Usa SOLO este contexto del dataset:

Resumen:
{contexto.get("resumen", "")}

Introducción:
{contexto.get("introduccion", "")}

Marco teórico:
{contexto.get("marco_teorico", "")}

Datos:
Título: {datos.get("titulo", "")}
Categoría: {datos.get("categoria", "")}
Objetivo: {datos.get("objetivo", "")}

Genera una versión mejorada y coherente del contenido.

Reglas:
- No inventes conceptos fuera del contexto.
- Mantén coherencia con el dataset.
- Conserva el tema físico original.
- Devuelve SOLO JSON válido.

Genera únicamente:
- resumen
- prologo
- introduccion
- marco_teorico

Formato:
{{
  "prologo": "",
  "resumen": "",
  "introduccion": "",
  "marco_teorico": ""
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Responde únicamente JSON válido."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    texto = response.choices[0].message.content

    return json.loads(texto)
