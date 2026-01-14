# Hiperbrains AI Job Description Maker

## Overview
This project is an AI-powered Job Description (JD) generator
It uses a locally hosted Large Language Model (LLM) to generate structured and professional job descriptions based on role inputs.

The project is backend-only and exposes REST APIs that can be consumed by an existing frontend (Angular).

---

## Key Features
- AI-generated job descriptions
- Structured output (Title, Summary, Responsibilities, Skills)
- Runs fully locally using Ollama (no paid APIs)
- REST API built with FastAPI
- Prompt-driven AI behavior

---

## Tech Stack
- **Backend**: FastAPI (Python)
- **AI Framework**: LangChain (Runnable-based API)
- **LLM**: Ollama (Mistral model)
- **API Testing**: Swagger / ReDoc / Postman

---

## Project Structure
hiperbrains-ai-jd-maker/
├── main.py # FastAPI application
├── jd_generator.py # AI logic (LangChain + Ollama)
├── prompts.py # Prompt template for JD generation
├── requirements.txt # Python dependencies
├── README.md # Project documentation


---

## Setup Instructions (Local)

### 1. Install Python
Recommended version: **Python 3.10 or 3.11**

---

### 2. Install Ollama
Download and install from:
https://ollama.com

Start the model:
```bash
ollama run mistral

last updated: 14/1/2026
