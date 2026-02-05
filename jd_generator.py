import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_job_description(role_details: str) -> str:
    payload = {
        "model": "mistral",
        "prompt": role_details,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    return response.json()["response"]
