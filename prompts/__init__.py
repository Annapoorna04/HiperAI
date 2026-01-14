from .job_title import JOB_TITLE_PROMPT
from .responsibilities import RESPONSIBILITIES_PROMPT
from .required_skills import REQUIRED_SKILLS_PROMPT

JD_PROMPT = f"""
You are an HR expert at Hiperbrains.

Use the following role details to generate a complete job description.

Role Details:
{{role_details}}

---

{JOB_TITLE_PROMPT}

{RESPONSIBILITIES_PROMPT}

{REQUIRED_SKILLS_PROMPT}
"""
