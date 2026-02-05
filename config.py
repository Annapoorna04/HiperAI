"""
Configuration settings for AI Job Description Generator
Centralized configuration for guardrails and application settings
"""

from typing import List
import os


class GuardrailsConfig:
    """Guardrails configuration settings"""
    
    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "10"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    
    # Input Validation
    INPUT_MIN_LENGTH: int = int(os.getenv("INPUT_MIN_LENGTH", "10"))
    INPUT_MAX_LENGTH: int = int(os.getenv("INPUT_MAX_LENGTH", "2000"))
    
    # Output Validation
    OUTPUT_MIN_LENGTH: int = int(os.getenv("OUTPUT_MIN_LENGTH", "100"))
    OUTPUT_MAX_LENGTH: int = int(os.getenv("OUTPUT_MAX_LENGTH", "5000"))
    
    # Content Filtering - Blacklist Patterns
    BLACKLIST_PATTERNS: List[str] = [
        r'\b(hack|exploit|inject|sql|script|xss|malware)\b',
        r'<script.*?>.*?</script>',
        r'(javascript:|data:text/html)',
        r'(\bDROP\b|\bDELETE\b|\bINSERT\b)\s+(TABLE|FROM|INTO)',
    ]
    
    # Content Filtering - Inappropriate Content Patterns
    INAPPROPRIATE_PATTERNS: List[str] = [
        r'\b(porn|xxx|sex|nude|nsfw)\b',
        r'\b(violence|kill|murder|terrorist)\b',
    ]
    
    # Enable/Disable specific guardrails
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    ENABLE_CONTENT_FILTERING: bool = os.getenv("ENABLE_CONTENT_FILTERING", "true").lower() == "true"
    ENABLE_INPUT_VALIDATION: bool = os.getenv("ENABLE_INPUT_VALIDATION", "true").lower() == "true"
    ENABLE_OUTPUT_VALIDATION: bool = os.getenv("ENABLE_OUTPUT_VALIDATION", "true").lower() == "true"


class AIModelConfig:
    """AI Model configuration settings"""
    
    # Ollama Settings
    MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "mistral")
    MODEL_TEMPERATURE: float = float(os.getenv("AI_MODEL_TEMPERATURE", "0.3"))
    MODEL_TIMEOUT: int = int(os.getenv("AI_MODEL_TIMEOUT", "60"))
    MODEL_MAX_TOKENS: int = int(os.getenv("AI_MODEL_MAX_TOKENS", "1500"))
    
    # Ollama Connection
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class AppConfig:
    """Application configuration settings"""
    
    # API Settings
    APP_TITLE: str = "Hiperbrains AI JD Maker"
    APP_DESCRIPTION: str = "AI-powered Job Description Generator with Guardrails"
    APP_VERSION: str = "2.0.0"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


# Create global config instances
guardrails_config = GuardrailsConfig()
ai_model_config = AIModelConfig()
app_config = AppConfig()
