from groq import Groq
import os
import json

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def validar_y_mejorar(contenido: dict,contexto:dict) ->dict:
    prompt = f"""
Eres un experto en física educativa. Mejora el siguiente contenido 
para un laboratorio de física universitario.

Titulo:{contexto.get('titulo','')}
Categoria:{contexto.get('categoria','')}
Objetivo:{contexto.get('objetivo','')}

Contenido actual:

-Resumen: {contenido.get('resumen','')}
-Prologo:{contenido.get('prologo','')}
-Introduccion:{contenido.get('introduccion','')}
-Marco teorico:{contenido.get('marco teorico','')}

Responde SOLO en JSON con estas claves exactas:
resumen, prologo, introduccion, marco_teorico
Sin texto adicional, sin markdown, solo el JSON.
"""
    
    try:
        respuesta=client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}],
            temperature=0.3,
            max_tokens=2000
        )

        texto = respuesta.choices[0].message.content.strip()

        if "```json" in texto:
            texto=texto.split("```json")[1].split("```json")[0].strip()
        elif "```" in texto:
            texto=texto.split("```")[1].split("```")[0].strip()

        resultado =json.loads(texto)
        resultado["coincidencia"]=contenido.get("conincidencia",0)
        return resultado
    
    except:
        return contenido



