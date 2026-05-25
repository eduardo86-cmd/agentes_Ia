def formatear_contenido(fila, score):
    if fila is None:
        return{
            "resumen":"No se encontro informacion.",
            "introduccion":"",
            "marco_teorico":"",
            "coincidencia":score

        }

    return{
        "resumen":fila.get("resumen",""),
        "introduccion":fila.get("introduccion",""),
        "marco_teorico":fila.get("marco_teorico",""),
        "coincidencia":score
    }

def formatear_actividades(datos):
    return{
        "actividades":[
            {
                "nivel":"basico",
                "descripcion":f"Actividad basica sobre{datos['titulo']}.",
                "categoria":datos["categoria"],
                "objetivo":datos["objetivo"],
                 "palabras_clave": datos["palabras_clave"],
                "titulo":datos["titulo"],
                "resumen": datos["resumen"]
            
            },
            {
                "nivel": "intermedio",
                "descripcion": f"Actividad práctica sobre {datos['titulo']}.",
                "categoria": datos["categoria"],
                "objetivo": datos["objetivo"],
                "palabras_clave": datos["palabras_clave"],
                "titulo": datos["titulo"],
                "resumen": datos["resumen"]

            },
            {
                "nivel": "avanzado",
                "descripcion": f"Actividad avanzada sobre {datos['titulo']}.",
                "categoria": datos["categoria"],
                "objetivo": datos["objetivo"],
                "palabras_clave": datos["palabras_clave"],
                "titulo": datos["titulo"],
                "resumen": datos["resumen"]
            }
        ]
    }

def formatear_detalle(datos):
    return{
      "objetivo_especifico": f"Desarrollar la actividad: {datos['descripcion']}",
        "materiales": [],
        "procedimiento": [],
        "formula": "",
        "tiempo_estimado": ""
    

}