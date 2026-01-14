from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from data_loader import load_jd_inputs

from prompts import JD_PROMPT


# Connect to Ollama (local LLM)
llm = Ollama(
    model="mistral",
    temperature=0.3
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["role_details"],
    template=JD_PROMPT
)

# New LangChain way (NO LLMChain, NO langchain.chains)
jd_chain = prompt | llm


def generate_job_description(role_details: str) -> str:
    return jd_chain.invoke({"role_details": role_details})

def generate_job_description_from_json(jd_id: str) -> str:
    data = load_jd_inputs()

    for jd in data["job_descriptions"]:
        if jd["id"] == jd_id:
            role_details = jd["role_details"]
            return jd_chain.invoke({"role_details": role_details})

    return "Job description not found"