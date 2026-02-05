from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import logging
from typing import Optional

from prompts import JD_PROMPT

logger = logging.getLogger(__name__)

# Connect to Ollama (local LLM) with guardrails
llm = Ollama(
    model="mistral",
    temperature=0.3,
    timeout=60,  # 60 seconds timeout to prevent hanging
    num_predict=1500,  # Limit max tokens to prevent excessively long outputs
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["role_details"],
    template=JD_PROMPT
)

# New LangChain way (NO LLMChain, NO langchain.chains)
jd_chain = prompt | llm


def generate_job_description(role_details: str) -> str:
    """
    Generate job description with error handling and guardrails
    
    Args:
        role_details: Sanitized role details from guardrails
        
    Returns:
        Generated job description
        
    Raises:
        Exception: If generation fails
    """
    try:
        logger.info("Invoking AI model for job description generation")
        result = jd_chain.invoke({"role_details": role_details})
        
        # Ensure result is a string
        if not isinstance(result, str):
            result = str(result)
        
        logger.info(f"Job description generated successfully. Length: {len(result)} chars")
        return result
        
    except TimeoutError as e:
        logger.error("AI model timeout exceeded")
        raise Exception("AI model took too long to respond. Please try again.")
        
    except ConnectionError as e:
        logger.error(f"Connection error with AI model: {str(e)}")
        raise Exception("Unable to connect to AI model. Please ensure Ollama is running.")
        
    except Exception as e:
        logger.error(f"Error generating job description: {str(e)}")
        raise Exception(f"Failed to generate job description: {str(e)}")
