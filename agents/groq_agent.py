import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


def parsear_json_seguro(texto):
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        inicio = texto.find("{")
        fin = texto.rfind("}") + 1

        if inicio == -1 or fin <= inicio:
            raise ValueError(f"La respuesta no contiene JSON válido:\n{texto}")

        return json.loads(texto[inicio:fin])


def construir_contexto(contexto):
    return f"""
CONTEXTO DEL DATASET:

Resumen:
{contexto.get("resumen", "")}

Introducción:
{contexto.get("introduccion", "")}

Marco teórico:
{contexto.get("marco_teorico", "")}
""".strip()


def construir_datos(datos):
    return f"""
DATOS:

Título: {datos.get("titulo", "")}
Categoría: {datos.get("categoria", "")}
Objetivo: {datos.get("objetivo", "")}
Nivel: {datos.get("nivel", "")}
Descripción: {datos.get("descripcion", "")}
""".strip()


def pedir_groq_json(prompt, temperature=0.2):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un generador estricto de JSON válido. "
                    "Nunca respondas con markdown, explicaciones ni texto fuera del JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    texto = response.choices[0].message.content.strip()
    return parsear_json_seguro(texto)


def pedir_groq_texto(prompt, temperature=0.2):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Devuelve únicamente el texto solicitado, sin explicaciones."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


def generar_detalle_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico especializado en física escolar para Fisikapp.

Tu tarea es generar el detalle completo de una actividad educativa de física.

REGLAS OBLIGATORIAS:
- Usa únicamente el contexto del dataset y los datos entregados.
- No inventes conceptos que no estén relacionados con el tema.
- No agregues fórmulas si el contexto no permite justificarlas.
- Si no hay suficientes fórmulas, devuelve "formulas": [].
- El procedimiento debe ser claro, práctico y ordenado.
- Los materiales deben ser realistas para una actividad escolar.
- El lenguaje debe ser adecuado para estudiantes.
- El tiempo estimado debe ser breve y realista.

{construir_contexto(contexto)}

{construir_datos(datos)}

SALIDA:
Devuelve únicamente JSON válido.

ESTRUCTURA EXACTA:
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

    return pedir_groq_json(prompt, temperature=0.2)


def generar_actividades_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico especializado en física escolar para Fisikapp.

Tu tarea es generar tres actividades educativas a partir del contexto entregado.

REGLAS OBLIGATORIAS:
- Usa únicamente el contexto del dataset y los datos entregados.
- No inventes conceptos fuera del tema.
- Las actividades deben ser coherentes con el objetivo.
- Cada actividad debe tener un nivel distinto.
- La actividad básica debe ser simple y guiada.
- La actividad intermedia debe requerir análisis.
- La actividad avanzada debe incluir mayor razonamiento o aplicación.
- El lenguaje debe ser claro y educativo.

{construir_contexto(contexto)}

{construir_datos(datos)}

SALIDA:
Devuelve únicamente JSON válido.

ESTRUCTURA EXACTA:
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

    return pedir_groq_json(prompt, temperature=0.2)


def generar_contenido_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico especializado en física escolar para Fisikapp.

Tu tarea es mejorar y estructurar el contenido académico de una unidad o actividad de física.

REGLAS OBLIGATORIAS:
- Usa únicamente el contexto del dataset y los datos entregados.
- No inventes conceptos fuera del contexto.
- Conserva el tema físico original.
- Mantén coherencia entre resumen, prólogo, introducción y marco teórico.
- Usa lenguaje académico claro, pero comprensible para estudiantes.
- Los conceptos básicos deben estar directamente relacionados con el tema.
- El campo "tipo" solo puede ser uno de estos valores:
  "teorico", "formula", "unidad", "instrumento", "fenomeno".

{construir_contexto(contexto)}

{construir_datos(datos)}

SALIDA:
Devuelve únicamente JSON válido.

ESTRUCTURA EXACTA:
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

    return pedir_groq_json(prompt, temperature=0.2)


def prompt_hooke(datos):
    titulo = datos.get("titulo", "").lower()
    descripcion = datos.get("descripcion", "").lower()
    categoria = datos.get("categoria", "").lower()

    if "hooke" in titulo or "resorte" in descripcion or "elongación" in descripcion or "elongacion" in descripcion:
        return (
            "Educational physics textbook illustration of Hooke's law experiment. "
            "A vertical metal spring hanging from a laboratory support stand, "
            "with calibrated masses attached to the bottom of the spring. "
            "A ruler is placed next to the spring to measure elongation. "
            "Simple arrows show weight downward and elastic restoring force upward. "
            "Clean white background, realistic school laboratory equipment, "
            "scientific infographic style, high quality, clear composition. "
            "Only show spring, calibrated masses, ruler, support stand, and arrows. "
            "No people, no hands, no fingers, no animals, no fish, no pencils, "
            "no books, no notebooks, no decorative objects, no table, no graph, "
            "no text, no labels, no letters, no numbers."
        )

    return None


def generar_prompt_imagen(datos):
    prompt_fijo = prompt_hooke(datos)

    if prompt_fijo:
        return prompt_fijo

    return f"""
Educational physics textbook illustration.

Topic:
{datos.get("titulo", "")}

Category:
{datos.get("categoria", "")}

Level:
{datos.get("nivel", "")}

Activity:
{datos.get("descripcion", "")}

Visual style:
Educational physics infographic, realistic school laboratory equipment, clean white background, scientific composition, clear arrows only if needed, high quality, textbook style.

Restrictions:
Only show the physics experiment. No people, no hands, no animals, no fish, no pencils, no books, no notebooks, no decorative objects, no unrelated cables, no unrelated generators, no table, no graph, no text, no labels, no letters, no numbers.
""".strip()


def generar_prompt_visual_con_groq(datos, contexto):
    prompt_fijo = prompt_hooke(datos)

    if prompt_fijo:
        return prompt_fijo

    prompt = f"""
Generate ONE short visual prompt in English for an image generation model.

TOPIC DATA:
Title: {datos.get("titulo", "")}
Category: {datos.get("categoria", "")}
Level: {datos.get("nivel", "")}
Objective: {datos.get("objetivo", "")}
Activity: {datos.get("descripcion", "")}

Dataset summary:
{contexto.get("resumen", "")}

MANDATORY RULES:
- Maximum 100 words.
- Write only in English.
- Do not explain.
- Do not use markdown.
- Describe only what should appear in the image.
- Represent only the physics experiment.
- Use realistic school laboratory instruments.
- Use a clean white background.
- Use an educational physics textbook illustration style.
- Use clear arrows only if they represent a physical phenomenon.
- Do not mention or show people.
- Do not mention or show hands.
- Do not mention or show fingers.
- Do not mention or show animals.
- Do not mention or show fish.
- Do not mention or show pencils.
- Do not mention or show books.
- Do not mention or show notebooks.
- Do not mention or show decorative objects.
- Do not mention tables or graphs.
- Do not include text, labels, letters or numbers inside the image.
- Do not mix Spanish words into the final prompt.
"""

    return pedir_groq_texto(prompt, temperature=0.1)


def generar_prompt_desde_procedimiento(detalle, datos):
    prompt_fijo = prompt_hooke(datos)

    if prompt_fijo:
        return prompt_fijo

    pasos = detalle.get("procedimiento", [])

    pasos_texto = "\n".join(
        [f"Step {i + 1}: {paso}" for i, paso in enumerate(pasos)]
    )

    prompt = f"""
Generate ONE short visual prompt in English for an educational physics image.

TOPIC:
{datos.get("titulo", "")}

CATEGORY:
{datos.get("categoria", "")}

ACTIVITY:
{datos.get("descripcion", "")}

PROCEDURE:
{pasos_texto}

MANDATORY RULES:
- Maximum 100 words.
- Represent only the physics experiment.
- Show the main equipment in the foreground.
- Show measurement instruments related to the activity.
- Show visual arrows only if they represent motion, force, heat, light or electric current.
- Use a clean white background.
- Use an educational physics textbook illustration style.
- Make it scientifically correct.
- Do not add decorative objects.
- Do not show people.
- Do not show hands.
- Do not show fingers.
- Do not show animals.
- Do not show fish.
- Do not show books.
- Do not show notebooks.
- Do not show pencils.
- Do not show handwriting.
- Do not show students writing.
- Do not include text inside the image.
- Do not include letters.
- Do not include numbers.
- Do not include labels.
- Do not split the image into panels.
- Do not add cables or generators unless the experiment is about electricity.
"""

    return pedir_groq_texto(prompt, temperature=0.1)


def limpiar_prompt_visual(prompt):
    palabras_prohibidas = [
        "hand",
        "hands",
        "finger",
        "fingers",
        "person",
        "people",
        "student",
        "students",
        "fish",
        "animal",
        "animals",
        "pencil",
        "book",
        "notebook",
        "table",
        "graph",
        "chart",
        "resorte"
    ]

    prompt_limpio = prompt

    for palabra in palabras_prohibidas:
        prompt_limpio = prompt_limpio.replace(palabra, "")

    return prompt_limpio.strip()


def generar_prompt_final_para_imagen(datos, contexto=None, detalle=None):
    contexto = contexto or {}

    prompt_fijo = prompt_hooke(datos)

    if prompt_fijo:
        prompt_final = prompt_fijo
    elif detalle:
        prompt_final = generar_prompt_desde_procedimiento(detalle, datos)
    else:
        prompt_final = generar_prompt_visual_con_groq(datos, contexto)

    prompt_final = limpiar_prompt_visual(prompt_final)

    restricciones = (
        " Only show the physics experiment. "
        "No people, no hands, no fingers, no animals, no fish, no pencils, "
        "no books, no notebooks, no decorative objects, no table, no graph, "
        "no text, no labels, no letters, no numbers."
    )

    return f"{prompt_final} {restricciones}".strip()