import requests
from urllib.parse import quote

def generar_imagen(prompt):
    prompt_url = quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=1024&height=1024&nologo=true"

    response = requests.get(url, timeout=120)

    if response.status_code != 200:
        raise Exception(f"Error generando imagen: {response.text}")

    return response.content