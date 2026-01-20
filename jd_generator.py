import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "mistral:latest"


def generate_job_description(role_details: str) -> str:
    prompt = f"""
You are an HR expert at Hiperbrains.

Generate a professional job description with:
- Role summary
- Responsibilities
- Required skills
- Nice-to-have skills

Role details:
{role_details}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        print("Calling Ollama...")
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print("Ollama error:", e)
        return "Error generating job description. Please try again."
