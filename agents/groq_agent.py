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
            raise ValueError(
                f"La respuesta no contiene JSON válido:\n{texto}"
            )

        bloque = texto[inicio:fin]

        # Corrige escapes inválidos generados por el modelo
        bloque = bloque.replace("\\'", "'")
        bloque = bloque.replace("\\\n", "\n")

        return json.loads(bloque)


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
                    "Devuelve únicamente JSON. "
                    "No uses markdown ni explicaciones. "
                    "No uses LaTeX. "
                    "Las fórmulas deben escribirse en texto plano usando * para multiplicación. "
                    "No agregues barra invertida antes de símbolos matemáticos."
                    
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

    print("========== RESPUESTA GROQ ==========")
    print(texto)
    print("====================================")

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
Eres un asistente académico especializado en la enseñanza de Física para estudiantes de grado noveno, décimo y undécimo de educación media en Colombia dentro de la plataforma Fisikapp.

Tu tarea es generar el contenido completo de UNA práctica de laboratorio de Física basada en la actividad seleccionada por el profesor.

La información generada será almacenada directamente en la base de datos de Fisikapp, por lo tanto debes respetar exactamente la estructura JSON solicitada.

==========================
REGLAS OBLIGATORIAS
==========================

- Usa únicamente el contexto del dataset y los datos entregados.
- No inventes conceptos que no estén relacionados con el tema.
- No agregues información que no pueda justificarse con el contexto.
- Utiliza un lenguaje claro, técnico y apropiado para estudiantes de educación media.
- El objetivo debe ser claro, específico y medible.
- La descripción debe explicar de manera breve en qué consiste la práctica.
- El nombre de la práctica debe ser corto, descriptivo y relacionado con el tema del laboratorio.
- Los materiales deben ser realistas y adecuados para una práctica escolar.
- Los procedimientos deben estar organizados cronológicamente.
- Cada procedimiento debe representar un único paso.
- No numeres los procedimientos.
- No escribas "Paso 1", "Paso 2", etc.
- Cada elemento del arreglo "procedimientos" representa un paso independiente.
- El campo "calculos" debe contener únicamente las operaciones matemáticas, ecuaciones o fórmulas que el estudiante deberá aplicar durante la práctica.
- No describas el procedimiento experimental en el campo "calculos".
- No repitas el objetivo ni la descripción en el campo "calculos".
- Si la práctica requiere cálculos, explica brevemente qué operación realizará el estudiante.
- Si la práctica no requiere cálculos, devuelve una cadena vacía ("").
- Genera únicamente las fórmulas necesarias para desarrollar la práctica.
- Si el tema requiere varias fórmulas, genera entre 1 y 5.
- Si el tema no requiere fórmulas, devuelve un arreglo vacío [].
- No cambies el nombre de ninguna clave.
- No agregues claves adicionales.
- No elimines ninguna clave.
- No utilices Markdown.
- No escribas ```json.
- No agregues comentarios.
- Devuelve únicamente un objeto JSON válido.

==========================
CONTEXTO
==========================

{construir_contexto(contexto)}

==========================
DATOS
==========================

{construir_datos(datos)}

==========================
SALIDA
==========================

Devuelve exactamente el siguiente formato JSON:

{{
    "nombre_practica": "",
    "objetivo": "",
    "descripcion": "",
    "materiales": [
        ""
    ],
    "calculos": "",
    "procedimientos": [
        ""
    ],
    "formulas": [
        {{
            "nombre": "",
            "descripcion": "",
            "expresion": ""
        }}
    ]
}}

==========================
IMPORTANTE
==========================

- "nombre_practica" debe ser un título corto y descriptivo relacionado con el tema del laboratorio.
- "objetivo" debe indicar claramente qué aprenderá o comprobará el estudiante.
- "descripcion" debe explicar brevemente en qué consiste la práctica.
- "materiales" debe contener únicamente los materiales necesarios para realizar la práctica.
- "calculos" debe describir únicamente las operaciones matemáticas o fórmulas que el estudiante aplicará durante la práctica. No debe contener pasos del procedimiento. Si no aplica, devolver una cadena vacía ("").
- "procedimientos" debe contener únicamente los pasos experimentales de la práctica.
- "formulas" debe contener únicamente las fórmulas necesarias para desarrollar la actividad.

Recuerda: la respuesta será almacenada directamente en la base de datos de Fisikapp. Debes respetar exactamente la estructura JSON indicada y responder únicamente con un objeto JSON válido.
"""
    
    return pedir_groq_json(prompt, temperature=0.2)



def generar_actividades_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico especializado en la enseñanza de Física para estudiantes de grado noveno, décimo y undécimo de educación media en Colombia dentro de la plataforma Fisikapp.

Tu tarea es generar tres actividades educativas para un laboratorio virtual de Física.

OBJETIVO:

Diseñar actividades que permitan al estudiante alcanzar el objetivo del laboratorio, fortalecer la comprensión de los conceptos físicos y desarrollar competencias científicas mediante un proceso de aprendizaje progresivo.

REGLAS OBLIGATORIAS:

- Utiliza el contexto del dataset como la principal referencia académica para garantizar el rigor científico del contenido generado.
- Utiliza los datos del laboratorio (título, categoría y objetivo) para adaptar el contenido al laboratorio específico que el docente está configurando.
- Todas las actividades deben estar directamente relacionadas con el título del laboratorio.
- Todas las actividades deben contribuir al cumplimiento del objetivo del laboratorio.
- Conserva el tema del laboratorio durante toda la generación.
- No inventes conceptos físicos que no estén respaldados por el contexto del dataset.
- No copies literalmente el contenido del dataset; úsalo como base para redactar actividades originales.
- Evita generar actividades genéricas que puedan utilizarse en cualquier laboratorio de Física.
- Cada actividad debe desarrollar un nivel diferente de complejidad.
- La actividad básica debe ser sencilla, guiada y enfocada en la comprensión inicial del tema.
- La actividad intermedia debe requerir análisis, interpretación o comparación de resultados.
- La actividad avanzada debe promover el razonamiento científico, la resolución de problemas o la aplicación de los conceptos aprendidos.
- Utiliza lenguaje académico claro, apropiado para estudiantes de educación media.
- Mantén coherencia entre las tres actividades, de manera que exista una progresión natural del aprendizaje.

CONTEXTO ACADÉMICO DEL DATASET

{construir_contexto(contexto)}

DATOS DEL LABORATORIO

{construir_datos(datos)}

IMPORTANTE:

El contexto del dataset proporciona la base conceptual del laboratorio.

Los datos del laboratorio determinan el tema específico para el cual deben diseñarse las actividades.

Si existe alguna diferencia entre el contexto recuperado y los datos del laboratorio, adapta las actividades utilizando el contexto como referencia académica, pero respetando siempre el título, la categoría y el objetivo del laboratorio.

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
Eres un asistente académico especializado en la enseñanza de Física para estudiantes de grado noveno, décimo y undécimo de educación media en Colombia dentro de la plataforma Fisikapp.
Tu tarea es mejorar y estructurar el contenido académico de una unidad o actividad de física.

OBJETIVO:
Generar contenido académico de calidad para un laboratorio virtual de Física, utilizando únicamente el contexto proporcionado y los datos recibidos.

REGLAS OBLIGATORIAS:
- Usa únicamente el contexto del dataset y los datos entregados.
- No inventes conceptos fuera del contexto.
- Conserva el tema físico original.
- Mantén coherencia entre resumen, prólogo, introducción y marco teórico.
- Usa lenguaje académico claro, pero comprensible para estudiantes.
- Los conceptos básicos deben estar directamente relacionados con el tema.
- El campo "tipo" solo puede ser uno de estos valores:
  "teorico", "formula", "unidad", "instrumento", "fenomeno".
- Cada campo debe tener suficiente información para ser utilizado como contenido académico, evitando respuestas demasiado cortas o excesivamente extensas.
- El marco teórico debe desarrollar los conceptos fundamentales del tema sin copiar literalmente el contexto recibido.
- Genera entre 4 y 8 conceptos básicos relevantes para el laboratorio.
- Evita repetir conceptos o definiciones similares entre los conceptos básicos.

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


def generar_portada_con_groq(datos, contexto):
    prompt = f"""
Eres un asistente académico especializado en física escolar para Fisikapp.

Tu tarea es generar la información inicial de un laboratorio virtual.

INSTRUCCIONES OBLIGATORIAS:

- Usa el contexto del dataset como fuente principal de información.
- Si el contexto no contiene suficiente información, puedes complementarla con conocimientos generales de física, siempre que sean correctos y coherentes con el tema.
- Mantén siempre coherencia entre el título, la categoría y el contexto recuperado.
- No cambies el tema principal del laboratorio.
- No inventes conceptos que no pertenezcan al tema.
- Utiliza un lenguaje académico, claro y apropiado para estudiantes.

DESCRIPCIÓN CORTA:
- Máximo 50 palabras.
- Debe resumir el propósito del laboratorio.
- Debe ser atractiva y fácil de entender.

OBJETIVO GENERAL:
- Debe comenzar con un verbo en infinitivo.
- Debe expresar claramente qué aprenderá el estudiante.

OBJETIVOS ESPECÍFICOS:
- Genera exactamente cuatro.
- Todos deben comenzar con un verbo en infinitivo.
- Deben contribuir al cumplimiento del objetivo general.
- No repitas ideas.
- Ordénalos de forma lógica.

{construir_contexto(contexto)}

DATOS:

Título:
{datos.get("titulo", "")}

Categoría:
{datos.get("categoria", "")}

SALIDA:

Devuelve únicamente JSON válido.

ESTRUCTURA EXACTA:

{{
    "descripcion_corta": "",
    "objetivo_general": "",
    "objetivos_especificos": [
        "",
        "",
        "",
        ""
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


def generar_prompt_portada(datos):
    titulo = datos.get("titulo", "")
    categoria = datos.get("categoria", "")

    return f"""
Educational physics textbook cover.

Topic:
{titulo}

Category:
{categoria}

Create a conceptual illustration representing the main physics topic.

Style:
Modern educational illustration.
Professional science textbook cover.
Clean laboratory environment.
High quality.
Realistic scientific equipment.
Soft lighting.
White or light background.

Rules:
- Represent only the main concept of the topic.
- Do not show the experiment procedure.
- Do not show steps.
- Do not include text.
- Do not include letters.
- Do not include numbers.
- Do not include labels.
- No decorative objects.
- Educational style.
""".strip()


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
Flat vector illustration, colorful educational infographic, cartoon science laboratory, cute student scientist, simple geometric shapes, bright colors, clean vector design, educational poster style, children textbook illustration, modern 2D flat design, icon-based laboratory elements, friendly character, high quality vector art.

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

- Use a clean white background.

- Use clear arrows only if they represent a physical phenomenon.
- Do not mention or show fingers.
- Do not mention or show animals.
- Do not mention or show fish.
- Do not mention or show pencils.
- Do not mention or show books.
- Do not mention or show notebooks.
- Do not mention or show decorative objects.
- Do not mention tables or graphs.
- Do not mix Spanish words into the final prompt.
- Show friendly cartoon student scientists.
- Use colorful infographic elements.
- Use a vertical educational poster layout.
- Do not include text, labels, letters or numbers inside the image.
- Use colorful cartoon laboratory instruments.
- Use modern flat vector educational illustration style.
- Use child-friendly science poster style.

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
- Use modern flat vector illustration style.
- Use colorful cartoon educational science style.
- Use simple geometric shapes.
- Use friendly student scientist characters.
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
        
        "finger",
        "fingers",
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
    " Educational physics infographic. "
    "Show the experiment procedure visually. "
    "Use colorful cartoon vector style. "
    "Show the sequence of steps through images only. "
    "No text. "
    "No labels. "
    "No letters. "
    "No numbers. "
    "Flat 2D educational illustration. "
    "Child-friendly science poster. "
    "Not realistic. "
    "Not photographic."
)

    return f"{prompt_final} {restricciones}".strip()


def filtrar_pasos_visuales(procedimiento):
    palabras_no_visuales = [
        "registra",
        "registrar",
        "calcula",
        "calcular",
        "analiza",
        "analizar",
        "discute",
        "discutir",
        "gráfico",
        "grafico",
        "tabla",
        "fórmula",
        "formula",
        "conclusión",
        "conclusion",
        "resultados"
    ]

    pasos_visuales = []

    for paso in procedimiento:
        paso_lower = paso.lower()

        if not any(palabra in paso_lower for palabra in palabras_no_visuales):
            pasos_visuales.append(paso)

    return pasos_visuales

def generar_prompt_desde_pasos_visuales(datos, pasos_visuales):

    pasos_texto = "\n".join(
        [f"Scene {i+1}: {paso}" for i, paso in enumerate(pasos_visuales)]
    )

    prompt = f"""
Create a modern flat vector educational science illustration.

Physics topic:
{datos.get("titulo", "")}

Activity:
{datos.get("descripcion", "")}

Show the procedure visually using these scenes:
{pasos_texto}

Visual style:
modern flat vector illustration,
minimal cartoon science lab,
simple student characters,
simple laboratory equipment,
soft shadows,
rounded geometric shapes,
clean white background,
turquoise, coral, yellow and dark blue color palette,
professional educational poster style,
friendly school science design,
not realistic,
not photographic,
not 3D render.


Modern 3D educational physics simulation.
Virtual laboratory environment.
Semi-realistic scientific equipment.
Interactive STEM learning platform style.
Professional educational visualization.
Clean futuristic laboratory.
Digital measurement interface overlays.
Blue technology background.
High-quality 3D render.
Scientific visualization.
Realistic materials and lighting.
Modern educational software appearance.

Rules:
No text paragraphs.
Minimal interface elements only.
Show measurements through digital indicators.
Focus on laboratory equipment.
Show only the experiment procedure.
Professional educational simulation style.
"""

    return prompt.strip()