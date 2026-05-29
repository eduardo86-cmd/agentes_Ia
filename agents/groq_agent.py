import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


def generar_detalle_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico de física para Fisikapp.

Usa únicamente este contexto del dataset:

Genera entre 2 y 5 fórmulas relacionadas con la actividad si el contexto lo permite.
Cada fórmula debe tener nombre, descripción y expresión.

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

Responde SOLO JSON válido con esta estructura:
{{
  "objetivo_especifico": "",
  "materiales": [],
  "procedimiento": [],
  "formulas": [
    {{
      "nombre": "",
      "descripcion": "",
      "expresion": ""
    }}
  ],
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

Además genera una lista de conceptos básicos relacionados con el tema.
Cada concepto debe incluir:
- concepto
- descripcion
- ejemplo
- tipo

El tipo puede ser: "teorico", "formula", "unidad", "instrumento" o "fenomeno".

Formato:
{{
  "prologo": "",
  "resumen": "",
  "introduccion": "",
  "marco_teorico": "",
  "conceptos_basicos": [
    {{
      "concepto": "",
      "descripcion": "",
      "ejemplo": "",
      "tipo": ""
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



def generar_prompt_imagen(datos):

    return f"""
    ilustracion educativa.
    tema:
    {datos.get("titulo","")}

    categoria:
    {datos.get("categoria","")}

    Nivel :
    {datos.get("nivel","")}

    Actividad:
    {datos.get("descripcion","")}

    Estilo:
    -educativo
    -cientifico
    -moderno 
    -laboratorio fisico
    -alta calidad
    -iluminacion profesional
    -diagramas claros
    
    """


