"""
Data models for Nvidia NeMo Guardrails.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Violation:
    """Represents a safety violation found in content."""
    
    rule_name: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    confidence: float  # 0.0 to 1.0
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


@dataclass
class SafetyResult:
    """Result of a content safety check."""
    
    safe: bool
    score: float  # 0.0 to 1.0, higher is safer
    violations: List[Violation]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class ValidationResult:
    """Result of output validation."""
    
    valid: bool
    issues: List[str]
    suggestions: List[str]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class Message:
    """Represents a message in a conversation."""
    
    content: str
    user_id: str
    timestamp: datetime
    message_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class Rule:
    """Represents a guardrails rule."""
    
    name: str
    description: str
    enabled: bool = True
    threshold: float = 0.8
    parameters: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow() 