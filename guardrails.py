"""
Guardrails Module for AI Job Description Generator
Provides input validation, content filtering, rate limiting, and output validation
"""

import re
import time
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, Optional[str]]:
        """Check if request is allowed based on rate limit"""
        now = time.time()
        
        # Clean old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.max_requests:
            return False, f"Rate limit exceeded. Max {self.max_requests} requests per {self.window_seconds} seconds."
        
        # Add current request
        self.requests[client_id].append(now)
        return True, None


class ContentFilter:
    """Filter inappropriate or malicious content"""
    
    # Blacklisted patterns (can be extended)
    BLACKLIST_PATTERNS = [
        r'\b(hack|exploit|inject|sql|script|xss|malware)\b',
        r'<script.*?>.*?</script>',
        r'(javascript:|data:text/html)',
        r'(\bDROP\b|\bDELETE\b|\bINSERT\b)\s+(TABLE|FROM|INTO)',
    ]
    
    # Inappropriate content patterns
    INAPPROPRIATE_PATTERNS = [
        r'\b(porn|xxx|sex|nude|nsfw)\b',
        r'\b(violence|kill|murder|terrorist)\b',
    ]
    
    def __init__(self):
        self.blacklist_regex = re.compile('|'.join(self.BLACKLIST_PATTERNS), re.IGNORECASE)
        self.inappropriate_regex = re.compile('|'.join(self.INAPPROPRIATE_PATTERNS), re.IGNORECASE)
    
    def is_safe(self, text: str) -> Tuple[bool, Optional[str]]:
        """Check if text is safe and appropriate"""
        
        # Check for malicious patterns
        if self.blacklist_regex.search(text):
            logger.warning(f"Malicious content detected: {text[:100]}")
            return False, "Input contains potentially malicious content"
        
        # Check for inappropriate content
        if self.inappropriate_regex.search(text):
            logger.warning(f"Inappropriate content detected: {text[:100]}")
            return False, "Input contains inappropriate content"
        
        return True, None
    
    def sanitize(self, text: str) -> str:
        """Sanitize input text"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might be harmful
        text = re.sub(r'[<>{}]', '', text)
        return text.strip()


class InputValidator:
    """Validate input parameters"""
    
    MIN_LENGTH = 10
    MAX_LENGTH = 2000
    
    @staticmethod
    def validate_role_details(role_details: str) -> Tuple[bool, Optional[str]]:
        """Validate role details input"""
        
        # Check if empty
        if not role_details or not role_details.strip():
            return False, "Role details cannot be empty"
        
        # Check length
        if len(role_details) < InputValidator.MIN_LENGTH:
            return False, f"Role details too short. Minimum {InputValidator.MIN_LENGTH} characters required"
        
        if len(role_details) > InputValidator.MAX_LENGTH:
            return False, f"Role details too long. Maximum {InputValidator.MAX_LENGTH} characters allowed"
        
        # Check if it contains at least some alphanumeric characters
        if not re.search(r'[a-zA-Z0-9]', role_details):
            return False, "Role details must contain valid text"
        
        return True, None
    
    @staticmethod
    def validate_job_title(title: str) -> bool:
        """Validate if text looks like a job title"""
        # Job title should have reasonable length and format
        return 3 <= len(title) <= 100 and bool(re.search(r'[a-zA-Z]', title))


class OutputValidator:
    """Validate AI-generated output"""
    
    REQUIRED_SECTIONS = [
        "Job Title",
        "Job Summary",
        "Responsibilities",
        "Skills"
    ]
    
    MIN_OUTPUT_LENGTH = 100
    MAX_OUTPUT_LENGTH = 5000
    
    @staticmethod
    def validate_output(output: str) -> Tuple[bool, Optional[str]]:
        """Validate AI-generated job description"""
        
        # Check length
        if len(output) < OutputValidator.MIN_OUTPUT_LENGTH:
            return False, "Generated output is too short"
        
        if len(output) > OutputValidator.MAX_OUTPUT_LENGTH:
            logger.warning(f"Output length exceeds maximum: {len(output)} chars")
            # Truncate instead of rejecting
            output = output[:OutputValidator.MAX_OUTPUT_LENGTH]
        
        # Check if output contains at least some expected sections
        sections_found = sum(
            1 for section in OutputValidator.REQUIRED_SECTIONS
            if section.lower() in output.lower()
        )
        
        if sections_found < 2:  # At least 2 sections should be present
            return False, "Generated output doesn't match expected format"
        
        return True, None
    
    @staticmethod
    def check_output_quality(output: str) -> Dict[str, any]:
        """Check quality metrics of the output"""
        return {
            "length": len(output),
            "word_count": len(output.split()),
            "sections_found": [
                section for section in OutputValidator.REQUIRED_SECTIONS
                if section.lower() in output.lower()
            ],
            "has_bullet_points": bool(re.search(r'[-•*]\s', output)),
            "quality_score": min(100, len(output.split()) / 5)  # Simple quality metric
        }


class GuardrailsManager:
    """Main guardrails manager that coordinates all validation"""
    
    def __init__(self, rate_limit: int = 10, rate_window: int = 60):
        self.rate_limiter = RateLimiter(max_requests=rate_limit, window_seconds=rate_window)
        self.content_filter = ContentFilter()
        self.input_validator = InputValidator()
        self.output_validator = OutputValidator()
        logger.info("Guardrails Manager initialized")
    
    def validate_request(self, client_id: str, role_details: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Comprehensive request validation
        Returns: (is_valid, sanitized_input, error_message)
        """
        
        # 1. Check rate limit
        allowed, error = self.rate_limiter.is_allowed(client_id)
        if not allowed:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return False, None, error
        
        # 2. Validate input format
        valid, error = self.input_validator.validate_role_details(role_details)
        if not valid:
            logger.warning(f"Input validation failed: {error}")
            return False, None, error
        
        # 3. Content filtering
        safe, error = self.content_filter.is_safe(role_details)
        if not safe:
            logger.warning(f"Content filter triggered: {error}")
            return False, None, error
        
        # 4. Sanitize input
        sanitized = self.content_filter.sanitize(role_details)
        
        logger.info(f"Request validated successfully for client: {client_id}")
        return True, sanitized, None
    
    def validate_output(self, output: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Validate AI-generated output
        Returns: (is_valid, error_message, quality_metrics)
        """
        
        valid, error = self.output_validator.validate_output(output)
        if not valid:
            logger.error(f"Output validation failed: {error}")
            return False, error, None
        
        # Get quality metrics
        quality = self.output_validator.check_output_quality(output)
        logger.info(f"Output validated successfully. Quality score: {quality['quality_score']}")
        
        return True, None, quality


# Global instance
guardrails = GuardrailsManager(rate_limit=10, rate_window=60)


def get_client_id(request: Request) -> str:
    """Extract client identifier from request"""
    # Use X-Forwarded-For if behind proxy, otherwise use client host
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
