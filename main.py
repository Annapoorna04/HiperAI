from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from jd_generator import generate_job_description

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JDRequest(BaseModel):
    role_details: str

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/generate-jd")
def generate_jd(req: JDRequest):
    jd = generate_job_description(req.role_details)
    return {"job_description": jd}
