"""
Main guardrails engine for AI safety checks.
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import SafetyResult, ValidationResult, Violation, Rule


class GuardrailsEngine:
    """Main engine for managing guardrails and safety checks."""
    
    def __init__(self, config_path: Optional[str] = None, rules: Optional[List[Rule]] = None):
        """
        Initialize the guardrails engine.
        
        Args:
            config_path: Path to configuration file
            rules: List of custom rules
        """
        self.config_path = config_path
        self.rules = rules or []
        self._initialized = False
        
    async def initialize(self) -> None:
        """Initialize the engine and load configuration."""
        if self._initialized:
            return
            
        # Load configuration if provided
        if self.config_path:
            await self._load_config()
            
        # Initialize default rules if none provided
        if not self.rules:
            self.rules = self._get_default_rules()
            
        self._initialized = True
    
    async def check_content(self, content: str, context: Optional[Dict[str, Any]] = None) -> SafetyResult:
        """
        Check content for safety violations.
        
        Args:
            content: Text content to check
            context: Additional context for the check
            
        Returns:
            SafetyResult with safety score and violations
        """
        if not self._initialized:
            await self.initialize()
            
        violations = []
        total_score = 1.0
        
        # Apply each rule
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            rule_result = await self._apply_rule(rule, content, context)
            if rule_result:
                violations.append(rule_result)
                # Reduce score based on violation severity
                severity_multiplier = self._get_severity_multiplier(rule_result.severity)
                total_score *= (1.0 - rule_result.confidence * severity_multiplier)
        
        # Ensure score is between 0 and 1
        total_score = max(0.0, min(1.0, total_score))
        
        return SafetyResult(
            safe=total_score >= 0.8 and len(violations) == 0,
            score=total_score,
            violations=violations,
            timestamp=datetime.utcnow(),
            metadata={"context": context}
        )
    
    async def validate_output(self, output: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate AI output against safety rules.
        
        Args:
            output: AI-generated output
            context: Additional context for validation
            
        Returns:
            ValidationResult with validation status
        """
        if not self._initialized:
            await self.initialize()
            
        issues = []
        suggestions = []
        
        # Check output length
        if len(output) > 10000:
            issues.append("Output is too long (max 10,000 characters)")
            suggestions.append("Consider breaking the response into smaller parts")
        
        # Check for common issues
        if not output.strip():
            issues.append("Output is empty or contains only whitespace")
            suggestions.append("Ensure the AI generates meaningful content")
        
        # Check content safety
        safety_result = await self.check_content(output, context)
        if not safety_result.safe:
            issues.append(f"Content safety check failed (score: {safety_result.score:.2f})")
            suggestions.append("Review and revise the output for safety concerns")
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
            timestamp=datetime.utcnow(),
            metadata={"context": context, "safety_score": safety_result.score}
        )
    
    async def _apply_rule(self, rule: Rule, content: str, context: Optional[Dict[str, Any]] = None) -> Optional[Violation]:
        """Apply a specific rule to content."""
        # This is a simplified implementation
        # In a real implementation, you would integrate with NeMo Guardrails
        
        # Example rule checking for harmful content
        harmful_keywords = ["harmful", "dangerous", "illegal", "inappropriate"]
        
        content_lower = content.lower()
        for keyword in harmful_keywords:
            if keyword in content_lower:
                return Violation(
                    rule_name=rule.name,
                    severity="medium",
                    description=f"Content contains potentially harmful keyword: {keyword}",
                    confidence=0.7,
                    context={"keyword": keyword, "rule_parameters": rule.parameters},
                    timestamp=datetime.utcnow()
                )
        
        return None
    
    def _get_severity_multiplier(self, severity: str) -> float:
        """Get multiplier for severity levels."""
        multipliers = {
            "low": 0.1,
            "medium": 0.3,
            "high": 0.6,
            "critical": 1.0
        }
        return multipliers.get(severity, 0.3)
    
    def _get_default_rules(self) -> List[Rule]:
        """Get default safety rules."""
        return [
            Rule(
                name="content_safety",
                description="Basic content safety check",
                enabled=True,
                threshold=0.8
            ),
            Rule(
                name="length_check",
                description="Check content length",
                enabled=True,
                threshold=0.9,
                parameters={"max_length": 10000}
            )
        ]
    
    async def _load_config(self) -> None:
        """Load configuration from file."""
        # Implementation would load from config_path
        pass 