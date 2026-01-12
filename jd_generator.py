from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

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
