from fastapi import FastAPI
from pydantic import BaseModel
from jd_generator import generate_job_description
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Hiperbrains AI JD Maker")

class JDRequest(BaseModel):
    role_details: str

@app.post("/generate-jd")
def generate_jd(req: JDRequest):
    jd = generate_job_description(req.role_details)
    return {"job_description": jd}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")
