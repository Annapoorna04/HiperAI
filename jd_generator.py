# # from langchain_community.llms import Ollama
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnableSequence
# from data.data_loader import load_jd_inputs

# from prompts import JD_PROMPT


# # Connect to Ollama (local LLM)
# # # llm = Ollama(
# #     model="mistral",
# #     temperature=0.3
# # )

# # Prompt template
# prompt = PromptTemplate(
#     input_variables=["role_details"],
#     template=JD_PROMPT
# )

# # New LangChain way (NO LLMChain, NO langchain.chains)
# jd_chain = prompt | llm


# def generate_job_description(role_details: str) -> str:
#     return jd_chain.invoke({"role_details": role_details})

# def generate_job_description_from_json(jd_id: str) -> str:
#     data = load_jd_inputs()

#     for jd in data["job_descriptions"]:
#         if jd["id"] == jd_id:
#             role_details = jd["role_details"]
#             return jd_chain.invoke({"role_details": role_details})

#     return "Job description not found"

# def generate_job_description(role_details: str) -> str:
#     return f"JD generated for role: {role_details}"
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


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

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    return response.json()["response"]
response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=120   # important
)
print("Calling Ollama...")
