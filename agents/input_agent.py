
import unicodedata


def limpiar_texto(texto):
    texto=str(texto).lower()
    texto=unicodedata.normalize("NFKD",texto)
    texto=texto.encode("ascii","ignore").decode("utf_8")
    return texto.strip()

def preparar_entrada(datos):
    return{
        "laboratorio_id": datos.get("laboratorio_id"),
        "categoria":limpiar_texto(datos.get("categoria","")),
        "objetivo":datos.get("objetivo",""),
        "palabras_clave":datos.get("palabras_clave",""),
        "titulo":datos.get("titulo",""),
        "resumen":datos.get("resumen",""),
        "nivel":datos.get("nivel",""),
        "descripcion":datos.get("descripcion","")

    }



