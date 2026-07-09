import pandas as pd
from rapidfuzz import fuzz
from agents.input_agent import limpiar_texto

df = pd.read_csv("data/dataset fisikapp.csv")
df.columns = df.columns.str.strip().str.lower()

def buscar_contexto(categoria, titulo="", objetivo=""):
    mejor_fila = None
    mejor_score = 0

    categoria_usuario = limpiar_texto(categoria)
    titulo_usuario = limpiar_texto(titulo)
    objetivo_usuario = limpiar_texto(objetivo)

    for _, fila in df.iterrows():
        categoria_csv = limpiar_texto(str(fila.get("categoria", "")))
        objetivo_csv = limpiar_texto(str(fila.get("objetivo", "")))
        titulo_csv = limpiar_texto( str(fila.get("titulo", "")))

        contenido_csv = limpiar_texto(
            str(fila.get("marco_teorico", "")) + " " +
            str(fila.get("resumen", "")) + " " +
            str(fila.get("introduccion", ""))
        )

        score_categoria = fuzz.partial_ratio(categoria_usuario, categoria_csv)
        score_titulo = fuzz.partial_ratio(titulo_usuario, titulo_csv)
        score_objetivo = fuzz.partial_ratio(objetivo_usuario, objetivo_csv)
        score_contenido = fuzz.partial_ratio(titulo_usuario,contenido_csv)

        score = (
        score_categoria * 0.20 +
        score_titulo * 0.40 +
        score_objetivo * 0.30 +
        score_contenido * 0.10
            )
        if score > mejor_score:
            mejor_score = score
            mejor_fila = fila

    if mejor_score < 40 or mejor_fila is None:
        return None, mejor_score
    

    print("\n=== CONTEXTO ENCONTRADO ===")
    print("Título:", mejor_fila.get("titulo", ""))
    print("Categoría:", mejor_fila.get("categoria", ""))
    print("Objetivo:", mejor_fila.get("objetivo", ""))
    print("Score:", round(mejor_score, 2))
    print("===========================\n")

    return mejor_fila, mejor_score