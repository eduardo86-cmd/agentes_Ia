
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

def preparar_entrada_evaluacion(datos):
    return {
        "laboratorio_id": datos.get("laboratorio_id"),
        "titulo": datos.get("titulo", ""),
        "categoria": limpiar_texto(datos.get("categoria", "")),
        "objetivo": datos.get("objetivo", ""),
        "estudiante": datos.get("estudiante", ""),

        # Práctica
        "observaciones": datos.get("observaciones", ""),
        "datos_obtenidos": datos.get("datos_obtenidos", {}),
        "conclusiones": datos.get("conclusiones", ""),

        # Simulación
        "completed": datos.get("completed"),
        "result_status": datos.get("result_status"),
        "best_attempt": datos.get("best_attempt"),
        "best_distance": datos.get("best_distance"),
        "average_distance": datos.get("average_distance"),
        "successful_attempts": datos.get("successful_attempts"),
        "failed_attempts": datos.get("failed_attempts"),
        "started_at": datos.get("started_at"),
        "finished_at": datos.get("finished_at"),
    }

