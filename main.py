from fastapi import FastAPI
from pydantic import BaseModel
from jd_generator import generate_job_description

app = FastAPI(
    title="Hiperbrains AI JD Maker",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

class JDRequest(BaseModel):
    role_details: str

@app.post("/generate-jd")
def generate_jd(request: JDRequest):
    jd = generate_job_description(request.role_details)
    return {
        "job_description": jd
    }
# {
# ...   "role_details": "Senior Backend Engineer, 5+ years, Python, Django, AWS, India"
# ... }
# name of the role
# experience
# technologies
# location