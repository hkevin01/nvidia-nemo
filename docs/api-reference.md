# API Reference

## Overview

This document provides comprehensive API documentation for the Nvidia NeMo Guardrails implementation.

## Core Modules

### Guardrails Engine

The core guardrails engine provides the main functionality for AI safety and content filtering.

#### `GuardrailsEngine`

Main class for managing guardrails and safety checks.

```python
class GuardrailsEngine:
    def __init__(self, config_path: str = None, rules: List[Rule] = None):
        """
        Initialize the guardrails engine.
        
        Args:
            config_path: Path to configuration file
            rules: List of custom rules
        """
        pass
    
    async def check_content(self, content: str) -> SafetyResult:
        """
        Check content for safety violations.
        
        Args:
            content: Text content to check
            
        Returns:
            SafetyResult with safety score and violations
        """
        pass
    
    async def validate_output(self, output: str, context: dict = None) -> ValidationResult:
        """
        Validate AI output against safety rules.
        
        Args:
            output: AI-generated output
            context: Additional context for validation
            
        Returns:
            ValidationResult with validation status
        """
        pass
```

#### `SafetyResult`

Result object containing safety check information.

```python
class SafetyResult:
    def __init__(self, score: float, violations: List[Violation], safe: bool):
        self.score = score  # Safety score (0-1)
        self.violations = violations  # List of violations found
        self.safe = safe  # Boolean indicating if content is safe
```

#### `ValidationResult`

Result object containing output validation information.

```python
class ValidationResult:
    def __init__(self, valid: bool, issues: List[str], suggestions: List[str]):
        self.valid = valid  # Whether output is valid
        self.issues = issues  # List of validation issues
        self.suggestions = suggestions  # List of improvement suggestions
```

### Conversation Management

#### `ConversationManager`

Manages conversation flow and context.

```python
class ConversationManager:
    def __init__(self, max_history: int = 100):
        """
        Initialize conversation manager.
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        pass
    
    async def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            message: Message object to add
        """
        pass
    
    async def get_context(self, window: int = 10) -> List[Message]:
        """
        Get recent conversation context.
        
        Args:
            window: Number of recent messages to include
            
        Returns:
            List of recent messages
        """
        pass
    
    async def check_conversation_safety(self) -> SafetyResult:
        """
        Check the entire conversation for safety violations.
        
        Returns:
            SafetyResult for the conversation
        """
        pass
```

### Configuration Management

#### `ConfigManager`

Manages guardrails configuration and rules.

```python
class ConfigManager:
    def __init__(self, config_path: str):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        pass
    
    def load_config(self) -> dict:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        pass
    
    def update_rules(self, rules: List[Rule]) -> None:
        """
        Update guardrails rules.
        
        Args:
            rules: New list of rules
        """
        pass
    
    def get_rule(self, rule_name: str) -> Rule:
        """
        Get a specific rule by name.
        
        Args:
            rule_name: Name of the rule
            
        Returns:
            Rule object
        """
        pass
```

## REST API Endpoints

### Content Safety

#### `POST /api/v1/safety/check`

Check content for safety violations.

**Request Body:**
```json
{
    "content": "Text content to check",
    "context": {
        "user_id": "user123",
        "session_id": "session456"
    }
}
```

**Response:**
```json
{
    "safe": true,
    "score": 0.95,
    "violations": [],
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### `POST /api/v1/safety/validate`

Validate AI output.

**Request Body:**
```json
{
    "output": "AI-generated output",
    "context": {
        "prompt": "Original prompt",
        "user_id": "user123"
    }
}
```

**Response:**
```json
{
    "valid": true,
    "issues": [],
    "suggestions": [],
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Conversation Management

#### `POST /api/v1/conversation/message`

Add a message to conversation.

**Request Body:**
```json
{
    "message": "User message content",
    "user_id": "user123",
    "session_id": "session456",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
    "message_id": "msg789",
    "safe": true,
    "added": true
}
```

#### `GET /api/v1/conversation/context/{session_id}`

Get conversation context.

**Response:**
```json
{
    "session_id": "session456",
    "messages": [
        {
            "id": "msg123",
            "content": "Message content",
            "user_id": "user123",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    ],
    "safe": true
}
```

### Configuration

#### `GET /api/v1/config/rules`

Get all active rules.

**Response:**
```json
{
    "rules": [
        {
            "name": "content_safety",
            "description": "Content safety rule",
            "enabled": true,
            "threshold": 0.8
        }
    ]
}
```

#### `PUT /api/v1/config/rules/{rule_name}`

Update a specific rule.

**Request Body:**
```json
{
    "enabled": true,
    "threshold": 0.9,
    "parameters": {
        "max_length": 1000
    }
}
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input provided",
        "details": {
            "field": "content",
            "issue": "Content cannot be empty"
        }
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `SAFETY_VIOLATION`: Content safety check failed
- `CONFIGURATION_ERROR`: Configuration issue
- `INTERNAL_ERROR`: Internal server error
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded

## Authentication

API endpoints support multiple authentication methods:

### API Key Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"content": "test"}' \
     http://localhost:8000/api/v1/safety/check
```

### JWT Authentication

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"content": "test"}' \
     http://localhost:8000/api/v1/safety/check
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per user
- **Premium**: 10000 requests per minute per user

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## WebSocket API

For real-time applications, WebSocket endpoints are available:

### `ws://localhost:8000/ws/safety`

Real-time content safety checking.

**Message Format:**
```json
{
    "type": "safety_check",
    "content": "Text to check",
    "request_id": "req123"
}
```

**Response:**
```json
{
    "type": "safety_result",
    "request_id": "req123",
    "safe": true,
    "score": 0.95,
    "violations": []
}
```

## SDK Usage

### Python SDK

```python
from nemo_guardrails import GuardrailsClient

# Initialize client
client = GuardrailsClient(api_key="your-api-key")

# Check content safety
result = await client.check_safety("Text content")
print(f"Safe: {result.safe}, Score: {result.score}")

# Validate output
validation = await client.validate_output("AI output")
print(f"Valid: {validation.valid}")
```

### JavaScript SDK

```javascript
import { GuardrailsClient } from '@nvidia/nemo-guardrails';

// Initialize client
const client = new GuardrailsClient('your-api-key');

// Check content safety
const result = await client.checkSafety('Text content');
console.log(`Safe: ${result.safe}, Score: ${result.score}`);

// Validate output
const validation = await client.validateOutput('AI output');
console.log(`Valid: ${validation.valid}`);
```

## Examples

### Basic Content Safety Check

```python
import asyncio
from nemo_guardrails import GuardrailsEngine

async def main():
    # Initialize engine
    engine = GuardrailsEngine()
    
    # Check content
    result = await engine.check_content("Hello, world!")
    
    if result.safe:
        print("Content is safe!")
    else:
        print(f"Content has {len(result.violations)} violations")

asyncio.run(main())
```

### Conversation Management

```python
import asyncio
from nemo_guardrails import ConversationManager, Message

async def main():
    # Initialize manager
    manager = ConversationManager()
    
    # Add messages
    await manager.add_message(Message("Hello", "user123"))
    await manager.add_message(Message("Hi there!", "bot"))
    
    # Get context
    context = await manager.get_context()
    print(f"Conversation has {len(context)} messages")
    
    # Check safety
    safety = await manager.check_conversation_safety()
    print(f"Conversation is safe: {safety.safe}")

asyncio.run(main())
```

## Best Practices

1. **Always check content safety** before processing user input
2. **Validate AI outputs** before returning to users
3. **Maintain conversation context** for better safety analysis
4. **Use appropriate rate limits** to prevent abuse
5. **Monitor and log** all safety checks for analysis
6. **Regularly update rules** based on new threats and patterns
7. **Test thoroughly** with various content types and edge cases 