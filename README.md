# Hiperbrains AI Job Description Maker

## Overview
This project is an AI-powered Job Description (JD) generator with comprehensive guardrails for safety and quality.
It uses a locally hosted Large Language Model (LLM) to generate structured and professional job descriptions based on role inputs.

The project is backend-only and exposes REST APIs that can be consumed by an existing frontend (Angular).

---

## Key Features
- 🤖 AI-generated job descriptions
- 📋 Structured output (Title, Summary, Responsibilities, Skills)
- 🏠 Runs fully locally using Ollama (no paid APIs)
- ⚡ REST API built with FastAPI
- 🎯 Prompt-driven AI behavior
- 🛡️ **NEW: Comprehensive Guardrails System**
  - Rate limiting protection
  - Input validation and sanitization
  - Content filtering (malicious & inappropriate content)
  - Output quality validation
  - Timeout protection
  - Comprehensive logging

---

## Tech Stack
- **Backend**: FastAPI (Python)
- **AI Framework**: LangChain (Runnable-based API)
- **LLM**: Ollama (Mistral model)
- **API Testing**: Swagger / ReDoc / Postman
- **Security**: Custom guardrails system

---

## Project Structure
```
hiperbrains-ai-jd-maker/
├── main.py              # FastAPI application with guardrails
├── jd_generator.py      # AI logic (LangChain + Ollama)
├── guardrails.py        # Guardrails system (validation, filtering, rate limiting)
├── config.py            # Configuration settings
├── prompts.py           # Prompt template for JD generation
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── GUARDRAILS.md        # Detailed guardrails documentation
```

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
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Guardrails System

This project includes a comprehensive guardrails system to ensure safe and high-quality AI-generated content.

For detailed information, see [GUARDRAILS.md](GUARDRAILS.md)

### Quick Overview:
- **Rate Limiting**: 10 requests per 60 seconds per client
- **Input Validation**: Length checks (10-2000 chars), format validation
- **Content Filtering**: Blocks malicious and inappropriate content
- **Output Validation**: Ensures quality and completeness (100-5000 chars)
- **Logging**: Comprehensive logging for monitoring and debugging

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

#### Generate Job Description (with Guardrails)
```bash
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{
    "role_details": "Senior Backend Engineer, 5+ years, Python, Django, AWS, India"
  }'
```

#### Response Format
```json
{
  "job_description": "Generated job description text...",
  "quality_metrics": {
    "length": 850,
    "word_count": 120,
    "sections_found": ["Job Title", "Job Summary", "Responsibilities", "Skills"],
    "has_bullet_points": true,
    "quality_score": 24.0
  },
  "message": "Job description generated successfully with guardrails validation"
}
```

---

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Configuration

Configure guardrails and application settings using environment variables or by editing `config.py`.

Example `.env` file:
```bash
# Rate Limiting
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60

# Input Validation
INPUT_MIN_LENGTH=10
INPUT_MAX_LENGTH=2000

# AI Model
AI_MODEL_NAME=mistral
AI_MODEL_TEMPERATURE=0.3
AI_MODEL_TIMEOUT=60

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## Testing Guardrails

### Test Valid Request
```bash
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "Senior Backend Engineer, 5+ years, Python, Django, AWS, India"}'
```

### Test Input Validation (Too Short)
```bash
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "Dev"}'
```

### Test Content Filtering
```bash
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "DROP TABLE users; Senior Developer"}'
```

### Test Rate Limiting
```bash
# Send 11 requests rapidly (should get rate limited on 11th)
for i in {1..11}; do
  curl -X POST "http://localhost:8000/generate-jd" \
    -H "Content-Type: application/json" \
    -d '{"role_details": "Senior Backend Engineer, 5+ years, Python"}' &
done
```

---

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Success
- **400 Bad Request**: Invalid input or content filter triggered
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: AI model error or output validation failed

---

## Security Best Practices

1. ✅ Rate limiting enabled by default
2. ✅ Input validation and sanitization
3. ✅ Content filtering for malicious patterns
4. ✅ Output validation for quality assurance
5. ✅ Comprehensive logging for security monitoring
6. ✅ Timeout protection to prevent resource exhaustion

For production deployment:
- Configure appropriate CORS origins
- Set up log aggregation and monitoring
- Consider additional authentication
- Review and update content filter patterns regularly

---

## Troubleshooting

**Issue**: Rate limit errors
- Solution: Wait 60 seconds or increase rate limit in config

**Issue**: Content filter false positives
- Solution: Review patterns in `guardrails.py` or `config.py`

**Issue**: AI model timeout
- Solution: Check Ollama service status with `ollama list`

**Issue**: Output validation failures
- Solution: Review AI prompt in `prompts.py`

---

## Future Enhancements

- [ ] AI-based content moderation
- [ ] Redis-based distributed rate limiting
- [ ] User authentication and authorization
- [ ] Real-time monitoring dashboard
- [ ] Advanced anomaly detection
- [ ] Multi-language support

---

## Support

For questions or issues:
1. Check the logs for detailed error messages
2. Review [GUARDRAILS.md](GUARDRAILS.md) for detailed documentation
3. Test with the examples provided above
4. Contact the development team

---

**Last Updated**: February 5, 2026  
**Version**: 2.0.0 (with Guardrails)
