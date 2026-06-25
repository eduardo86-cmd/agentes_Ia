import os
import base64
from openai import OpenAI



def generar_imagen(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1
    )

    imagen_base64 = response.data[0].b64_json
    return base64.b64decode(imagen_base64)

def generar_imagen_base64(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1
    )

    return response.data[0].b64_json