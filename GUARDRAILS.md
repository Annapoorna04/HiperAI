# AI Model Guardrails Documentation

## Overview

This document describes the comprehensive guardrails system implemented for the Hiperbrains AI Job Description Generator. These guardrails ensure safe, reliable, and high-quality AI-generated content.

---

## Guardrails Components

### 1. **Rate Limiting**

Protects the API from abuse and ensures fair resource usage.

- **Default Limit**: 10 requests per 60 seconds per client
- **Identification**: Based on client IP address (supports X-Forwarded-For for proxies)
- **Response**: HTTP 429 (Too Many Requests) when limit exceeded
- **Configuration**: Adjustable via environment variables

**Environment Variables:**
```bash
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
```

---

### 2. **Input Validation**

Ensures all inputs meet quality and safety standards before processing.

**Validation Checks:**
- ✅ Non-empty input
- ✅ Minimum length: 10 characters
- ✅ Maximum length: 2000 characters
- ✅ Contains alphanumeric characters
- ✅ Proper text format

**Configuration:**
```bash
INPUT_MIN_LENGTH=10
INPUT_MAX_LENGTH=2000
```

---

### 3. **Content Filtering**

Blocks malicious and inappropriate content using pattern matching.

**Blocked Content Types:**

#### Malicious Patterns:
- SQL injection attempts (`DROP TABLE`, `DELETE FROM`, etc.)
- XSS attacks (`<script>`, `javascript:`, etc.)
- Code injection attempts
- System exploitation keywords

#### Inappropriate Content:
- Explicit/adult content
- Violence-related terms
- Discriminatory language
- Terrorism-related content

**Response:** HTTP 400 (Bad Request) with descriptive error message

---

### 4. **Input Sanitization**

Automatically cleans and normalizes input before AI processing.

**Sanitization Steps:**
- Remove HTML tags
- Strip excessive whitespace
- Remove potentially harmful special characters
- Normalize text format

---

### 5. **Output Validation**

Validates AI-generated content for quality and completeness.

**Validation Checks:**
- ✅ Minimum output length (100 characters)
- ✅ Maximum output length (5000 characters)
- ✅ Contains expected sections (Job Title, Summary, Responsibilities, Skills)
- ✅ Proper format and structure

**Quality Metrics Provided:**
- Output length
- Word count
- Sections detected
- Has bullet points
- Overall quality score

**Configuration:**
```bash
OUTPUT_MIN_LENGTH=100
OUTPUT_MAX_LENGTH=5000
```

---

### 6. **AI Model Protection**

Prevents AI model misuse and ensures reliability.

**Protection Mechanisms:**
- ⏱️ **Timeout Protection**: 60-second timeout prevents hanging
- 🔢 **Token Limiting**: Maximum 1500 tokens prevents excessive generation
- 🌡️ **Temperature Control**: 0.3 temperature ensures consistent output
- 🔄 **Error Handling**: Graceful handling of model failures

---

### 7. **Logging and Monitoring**

Comprehensive logging for security and debugging.

**Logged Events:**
- All API requests with client IDs
- Rate limit violations
- Content filter triggers
- Validation failures
- AI generation success/failure
- Output quality metrics

**Log Levels:**
- INFO: Normal operations
- WARNING: Rejected requests, validation failures
- ERROR: System errors, AI model failures

---

## API Response Formats

### Success Response

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

### Error Responses

#### Rate Limit Exceeded (429)
```json
{
  "detail": "Rate limit exceeded. Max 10 requests per 60 seconds."
}
```

#### Invalid Input (400)
```json
{
  "detail": "Role details too short. Minimum 10 characters required"
}
```

#### Content Filter Triggered (400)
```json
{
  "detail": "Input contains potentially malicious content"
}
```

#### Output Validation Failed (500)
```json
{
  "detail": "Generated content validation failed: Generated output is too short"
}
```

---

## Configuration Guide

### Environment Variables

Create a `.env` file in the project root:

```bash
# Rate Limiting
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60

# Input Validation
INPUT_MIN_LENGTH=10
INPUT_MAX_LENGTH=2000

# Output Validation
OUTPUT_MIN_LENGTH=100
OUTPUT_MAX_LENGTH=5000

# AI Model
AI_MODEL_NAME=mistral
AI_MODEL_TEMPERATURE=0.3
AI_MODEL_TIMEOUT=60
AI_MODEL_MAX_TOKENS=1500
OLLAMA_BASE_URL=http://localhost:11434

# Application
LOG_LEVEL=INFO
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=*

# Feature Flags
ENABLE_RATE_LIMITING=true
ENABLE_CONTENT_FILTERING=true
ENABLE_INPUT_VALIDATION=true
ENABLE_OUTPUT_VALIDATION=true
```

---

## Testing Guardrails

### Test Rate Limiting

```bash
# Send 11 requests rapidly (should get rate limited on 11th)
for i in {1..11}; do
  curl -X POST "http://localhost:8000/generate-jd" \
    -H "Content-Type: application/json" \
    -d '{"role_details": "Senior Backend Engineer, 5+ years, Python"}' &
done
```

### Test Input Validation

```bash
# Too short input
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "Dev"}'

# Too long input (>2000 chars)
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d "{\"role_details\": \"$(python -c 'print("A" * 2001)')\"}"
```

### Test Content Filtering

```bash
# Malicious content
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "DROP TABLE users; Senior Developer"}'

# Inappropriate content
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "This is inappropriate content for violence"}'
```

### Test Valid Input

```bash
# Valid request
curl -X POST "http://localhost:8000/generate-jd" \
  -H "Content-Type: application/json" \
  -d '{"role_details": "Senior Backend Engineer, 5+ years, Python, Django, AWS, India"}'
```

---

## Best Practices

### For Developers

1. **Always log guardrails events** for security monitoring
2. **Regularly update content filter patterns** to catch new threats
3. **Monitor rate limit violations** for potential attacks
4. **Review quality metrics** to improve AI prompts
5. **Test guardrails** before deploying changes

### For Deployment

1. **Set appropriate rate limits** based on expected traffic
2. **Configure CORS properly** for production
3. **Use environment variables** for sensitive configuration
4. **Enable all guardrails** in production
5. **Set up log aggregation** for monitoring

### For Frontend Integration

1. **Handle all error responses** gracefully
2. **Show meaningful error messages** to users
3. **Implement client-side validation** to reduce rejected requests
4. **Display quality metrics** to users (optional)
5. **Respect rate limits** with client-side throttling

---

## Monitoring and Alerts

### Key Metrics to Monitor

- **Rate Limit Hits**: High rate limit hits may indicate abuse
- **Content Filter Triggers**: Track blocked malicious attempts
- **Validation Failures**: High failures may indicate UX issues
- **AI Model Timeouts**: May indicate performance problems
- **Quality Scores**: Track output quality over time

### Recommended Alerts

- Alert when rate limit violations exceed threshold (e.g., 100/hour)
- Alert on repeated content filter triggers from same IP
- Alert on AI model timeout rate > 5%
- Alert on output validation failure rate > 10%

---

## Troubleshooting

### Common Issues

**Issue**: All requests getting rate limited
- **Solution**: Increase `RATE_LIMIT_MAX_REQUESTS` or `RATE_LIMIT_WINDOW_SECONDS`

**Issue**: Valid inputs being rejected by content filter
- **Solution**: Review and refine `BLACKLIST_PATTERNS` in `config.py`

**Issue**: AI model timeouts
- **Solution**: Increase `AI_MODEL_TIMEOUT` or check Ollama service

**Issue**: Output validation failures
- **Solution**: Review AI prompt to ensure proper output format

---

## Security Considerations

1. **IP-based rate limiting** can be bypassed with proxies/VPNs
   - Consider additional authentication for sensitive deployments
   
2. **Pattern-based filtering** may have false positives/negatives
   - Regularly update patterns based on real-world usage
   
3. **In-memory rate limiting** resets on server restart
   - Consider Redis-based rate limiting for production
   
4. **Logs may contain sensitive data**
   - Implement log sanitization for PII

---

## Future Enhancements

- [ ] AI-based content moderation (e.g., OpenAI Moderation API)
- [ ] Redis-based distributed rate limiting
- [ ] Advanced anomaly detection
- [ ] User authentication and role-based access
- [ ] Real-time monitoring dashboard
- [ ] Automatic threat blocking
- [ ] A/B testing for guardrails effectiveness

---

## Support

For questions or issues with guardrails:
1. Check logs for detailed error messages
2. Review configuration settings
3. Test with the examples provided
4. Contact the development team

---

**Last Updated**: February 5, 2026
**Version**: 2.0.0
