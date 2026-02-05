from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from jd_generator import generate_job_description
from guardrails import guardrails, get_client_id
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hiperbrains AI JD Maker",
    description="AI-powered Job Description Generator with Guardrails",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JDRequest(BaseModel):
    role_details: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Detailed job role information including title, experience, skills, and location",
        example="Senior Backend Engineer, 5+ years, Python, Django, AWS, India"
    )


class JDResponse(BaseModel):
    job_description: str
    quality_metrics: dict
    message: str = "Job description generated successfully"


class ErrorResponse(BaseModel):
    error: str
    detail: str


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Hiperbrains AI JD Maker",
        "version": "2.0.0",
        "guardrails": "enabled"
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "components": {
            "api": "operational",
            "guardrails": "active",
            "ai_model": "ready"
        }
    }


@app.post("/generate-jd", response_model=JDResponse, responses={
    429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
    400: {"model": ErrorResponse, "description": "Invalid input"},
    422: {"model": ErrorResponse, "description": "Validation error"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def generate_jd(request: JDRequest, req: Request):
    """
    Generate a professional job description with AI
    
    This endpoint includes multiple guardrails:
    - Rate limiting (10 requests per 60 seconds per client)
    - Input validation and sanitization
    - Content filtering (inappropriate and malicious content)
    - Output validation
    - Quality metrics
    """
    
    try:
        # Get client identifier
        client_id = get_client_id(req)
        logger.info(f"Request received from client: {client_id}")
        
        # Apply guardrails
        is_valid, sanitized_input, error_message = guardrails.validate_request(
            client_id=client_id,
            role_details=request.role_details
        )
        
        if not is_valid:
            logger.warning(f"Guardrails rejected request: {error_message}")
            
            # Determine appropriate status code
            if "rate limit" in error_message.lower():
                status_code = 429
            else:
                status_code = 400
            
            raise HTTPException(
                status_code=status_code,
                detail=error_message
            )
        
        # Generate job description with sanitized input
        logger.info("Generating job description...")
        jd = generate_job_description(sanitized_input)
        
        # Validate output
        output_valid, output_error, quality_metrics = guardrails.validate_output(jd)
        
        if not output_valid:
            logger.error(f"Output validation failed: {output_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Generated content validation failed: {output_error}"
            )
        
        logger.info("Job description generated successfully")
        
        return JDResponse(
            job_description=jd,
            quality_metrics=quality_metrics,
            message="Job description generated successfully with guardrails validation"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


# Example request body:
# {
#   "role_details": "Senior Backend Engineer, 5+ years, Python, Django, AWS, India"
# }
