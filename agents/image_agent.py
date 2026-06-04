import os
import requests
from urllib.parse import quote
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

hf_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)


def generar_imagen_pollinations(prompt):
    prompt_url = quote(prompt[:600])

    url = (
        f"https://image.pollinations.ai/prompt/{prompt_url}"
        "?width=1024&height=1024&nologo=true"
    )

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    return response.content


def generar_imagen_huggingface(prompt):
    image = hf_client.text_to_image(
        prompt=prompt[:1000],
        model="black-forest-labs/FLUX.1-schnell"
    )

    import io
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


def generar_imagen(prompt):
    try:
        print("Intentando generar imagen con Pollinations...")
        return generar_imagen_pollinations(prompt)

    except Exception as e:
        print("Pollinations falló:", e)
        print("Intentando generar imagen con Hugging Face...")

        return generar_imagen_huggingface(prompt)