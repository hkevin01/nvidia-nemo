"""
NeMo Guardrails Protection Examples

This module contains three concrete examples demonstrating how NeMo Guardrails
protects against common AI safety issues compared to unprotected implementations.
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

from .models import SafetyResult, ValidationResult, Violation, Message, Rule
from .engine import GuardrailsEngine
from .conversation import ConversationManager
from .config import ConfigManager


@dataclass
class ProtectionResult:
    """Result of a protection check."""
    success: bool
    blocked: bool
    reason: Optional[str] = None
    safety_score: float = 1.0
    original_content: Optional[str] = None
    safe_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentSafetyProtection:
    """Example 1: Content Safety and Harmful Output Prevention."""
    
    def __init__(self):
        self.engine = GuardrailsEngine()
        self.setup_safety_rules()
    
    def setup_safety_rules(self):
        """Configure safety rules for harmful content detection."""
        harmful_patterns = [
            "hack", "exploit", "bypass", "unauthorized access",
            "malware", "virus", "phishing", "social engineering",
            "bomb", "weapon", "illegal", "criminal", "fraud"
        ]
        
        # Add custom rule for harmful content
        harmful_rule = Rule(
            name="harmful_instructions",
            description="Detect and block harmful or illegal instructions",
            enabled=True,
            threshold=0.7,
            parameters={"harmful_keywords": harmful_patterns}
        )
        
        self.engine.rules.append(harmful_rule)
    
    async def check_harmful_content(self, content: str) -> ProtectionResult:
        """Check if content contains harmful instructions."""
        safety_result = await self.engine.check_content(content)
        
        if not safety_result.safe:
            return ProtectionResult(
                success=False,
                blocked=True,
                reason="Harmful content detected",
                safety_score=safety_result.score,
                original_content=content,
                safe_content="I cannot provide instructions for harmful or illegal activities.",
                metadata={"violations": [v.description for v in safety_result.violations]}
            )
        
        return ProtectionResult(
            success=True,
            blocked=False,
            safety_score=safety_result.score,
            original_content=content,
            safe_content=content
        )
    
    async def generate_safe_response(self, prompt: str) -> ProtectionResult:
        """Generate AI response with safety checks."""
        # Check input safety
        input_check = await self.check_harmful_content(prompt)
        if input_check.blocked:
            return input_check
        
        # Simulate AI response generation
        # In a real implementation, this would call an AI API
        ai_response = self._simulate_ai_response(prompt)
        
        # Check output safety
        output_check = await self.check_harmful_content(ai_response)
        if output_check.blocked:
            return ProtectionResult(
                success=False,
                blocked=True,
                reason="Unsafe AI output detected",
                safety_score=output_check.safety_score,
                original_content=ai_response,
                safe_content="I apologize, but I cannot provide that information as it may be harmful.",
                metadata={"original_response": ai_response}
            )
        
        return ProtectionResult(
            success=True,
            blocked=False,
            safety_score=output_check.safety_score,
            original_content=prompt,
            safe_content=ai_response
        )
    
    def _simulate_ai_response(self, prompt: str) -> str:
        """Simulate AI response generation."""
        # This is a simplified simulation
        if "hack" in prompt.lower():
            return "Here's how to hack into a system: First, you need to..."
        elif "bomb" in prompt.lower():
            return "To make a bomb, you'll need the following materials..."
        else:
            return "I'd be happy to help you with that question in a safe and legal way."


class PrivacyProtection:
    """Example 2: Personal Information Protection."""
    
    def __init__(self):
        self.engine = GuardrailsEngine()
        self.conversation_manager = ConversationManager()
        self.setup_privacy_rules()
    
    def setup_privacy_rules(self):
        """Configure privacy protection rules."""
        pii_patterns = {
            "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "address": r"\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b"
        }
        
        privacy_rule = Rule(
            name="pii_protection",
            description="Detect and redact personal information",
            enabled=True,
            threshold=0.8,
            parameters={"pii_patterns": pii_patterns}
        )
        
        self.engine.rules.append(privacy_rule)
    
    def redact_pii(self, text: str) -> Tuple[str, List[str]]:
        """Remove or redact personal information."""
        redacted_text = text
        detected_pii = []
        
        # Credit card numbers
        credit_card_pattern = r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
        if re.search(credit_card_pattern, text):
            redacted_text = re.sub(credit_card_pattern, "[CREDIT_CARD]", redacted_text)
            detected_pii.append("credit_card")
        
        # Social Security Numbers
        ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
        if re.search(ssn_pattern, text):
            redacted_text = re.sub(ssn_pattern, "[SSN]", redacted_text)
            detected_pii.append("ssn")
        
        # Email addresses
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.search(email_pattern, text):
            redacted_text = re.sub(email_pattern, "[EMAIL]", redacted_text)
            detected_pii.append("email")
        
        # Phone numbers
        phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        if re.search(phone_pattern, text):
            redacted_text = re.sub(phone_pattern, "[PHONE]", redacted_text)
            detected_pii.append("phone")
        
        # Addresses
        address_pattern = r"\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b"
        if re.search(address_pattern, text):
            redacted_text = re.sub(address_pattern, "[ADDRESS]", redacted_text)
            detected_pii.append("address")
        
        return redacted_text, detected_pii
    
    async def process_message_safely(self, user_message: str, user_id: str) -> ProtectionResult:
        """Process user message with privacy protection."""
        # Check for PII in input
        pii_check = await self.engine.check_content(user_message)
        
        # Redact PII before processing
        safe_message, detected_pii = self.redact_pii(user_message)
        
        # Store redacted message
        message = Message(
            content=safe_message,
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
        await self.conversation_manager.add_message(message)
        
        # Generate response with privacy-aware prompt
        system_prompt = """You are a helpful assistant. Never repeat, reference, or ask for personal information like credit card numbers, SSNs, or other sensitive data."""
        
        # Simulate AI response generation
        ai_response = self._simulate_ai_response(safe_message, system_prompt)
        
        # Check response for PII
        response_safety = await self.engine.check_content(ai_response)
        if not response_safety.safe:
            ai_response = "I apologize, but I cannot provide that information as it may contain sensitive data."
        
        return ProtectionResult(
            success=True,
            blocked=False,
            safety_score=response_safety.score,
            original_content=user_message,
            safe_content=ai_response,
            metadata={
                "pii_detected": len(detected_pii) > 0,
                "detected_pii_types": detected_pii,
                "safe_message": safe_message
            }
        )
    
    def _simulate_ai_response(self, message: str, system_prompt: str) -> str:
        """Simulate AI response generation with privacy awareness."""
        # This is a simplified simulation
        if "[CREDIT_CARD]" in message or "[SSN]" in message:
            return "I can help you with general questions, but I cannot process or store personal information like credit card numbers or SSNs."
        elif "[EMAIL]" in message:
            return "I notice you mentioned an email address. I'll help you while keeping your information private."
        else:
            return "I'd be happy to help you with that question while maintaining your privacy."


class FairnessProtection:
    """Example 3: Bias and Fairness Protection."""
    
    def __init__(self):
        self.engine = GuardrailsEngine()
        self.setup_fairness_rules()
        self.evaluation_history = []
    
    def setup_fairness_rules(self):
        """Configure fairness and bias protection rules."""
        protected_attributes = ["gender", "age", "race", "ethnicity", "religion", "nationality"]
        
        fairness_rule = Rule(
            name="fairness_protection",
            description="Detect and prevent bias in evaluations",
            enabled=True,
            threshold=0.8,
            parameters={"protected_attributes": protected_attributes}
        )
        
        self.engine.rules.append(fairness_rule)
    
    def extract_relevant_info(self, candidate_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract only job-relevant information."""
        return {
            "education": candidate_info.get("education", ""),
            "experience": candidate_info.get("experience", ""),
            "skills": candidate_info.get("skills", []),
            "projects": candidate_info.get("projects", []),
            "certifications": candidate_info.get("certifications", []),
            "achievements": candidate_info.get("achievements", [])
        }
    
    def check_for_bias_indicators(self, evaluation_text: str) -> Tuple[bool, List[str]]:
        """Check if evaluation contains bias indicators."""
        bias_indicators = [
            "young", "old", "male", "female", "diverse", "traditional",
            "aggressive", "assertive", "emotional", "logical", "cultural",
            "foreign", "native", "experienced", "inexperienced", "mature",
            "immature", "professional", "unprofessional"
        ]
        
        text_lower = evaluation_text.lower()
        found_indicators = [indicator for indicator in bias_indicators if indicator in text_lower]
        
        return len(found_indicators) > 0, found_indicators
    
    def calculate_fairness_score(self, evaluation: str, candidate_info: Dict[str, Any]) -> float:
        """Calculate fairness score based on evaluation quality."""
        bias_indicators = [
            "young", "old", "male", "female", "diverse", "traditional",
            "aggressive", "assertive", "emotional", "logical"
        ]
        text_lower = evaluation.lower()
        
        bias_count = sum(1 for indicator in bias_indicators if indicator in text_lower)
        fairness_score = max(0, 1.0 - (bias_count * 0.15))
        
        return fairness_score
    
    def extract_recommendation(self, evaluation: str) -> str:
        """Extract hiring recommendation from evaluation text."""
        evaluation_lower = evaluation.lower()
        
        if "hire" in evaluation_lower and "don't" not in evaluation_lower:
            return "Hire"
        elif "don't hire" in evaluation_lower or "reject" in evaluation_lower:
            return "Don't Hire"
        else:
            return "Further Review"
    
    async def evaluate_candidate_fairly(self, candidate_info: Dict[str, Any]) -> ProtectionResult:
        """Evaluate job candidate with fairness protection."""
        # Extract only relevant information
        relevant_info = self.extract_relevant_info(candidate_info)
        
        # Create bias-free prompt
        prompt = f"""
        Evaluate this job candidate for a software engineering position based ONLY on job-relevant criteria:
        
        Education: {relevant_info['education']}
        Experience: {relevant_info['experience']}
        Skills: {', '.join(relevant_info['skills'])}
        Projects: {', '.join(relevant_info['projects'])}
        Certifications: {', '.join(relevant_info['certifications'])}
        Achievements: {', '.join(relevant_info['achievements'])}
        
        Provide a structured evaluation with:
        1. Technical assessment (1-10)
        2. Experience assessment (1-10)
        3. Skills assessment (1-10)
        4. Overall recommendation (Hire/Don't Hire)
        5. Reasoning based ONLY on technical and professional qualifications
        
        Do NOT consider personal characteristics like age, gender, race, or ethnicity.
        """
        
        # Simulate AI evaluation
        evaluation = self._simulate_ai_evaluation(prompt, relevant_info)
        
        # Check for bias in the evaluation
        bias_detected, bias_indicators = self.check_for_bias_indicators(evaluation)
        
        if bias_detected:
            # Regenerate evaluation with stronger bias prevention
            bias_free_prompt = f"""
            Re-evaluate this candidate focusing ONLY on technical qualifications:
            
            Education: {relevant_info['education']}
            Experience: {relevant_info['experience']}
            Skills: {', '.join(relevant_info['skills'])}
            
            Provide a purely technical assessment without any personal characteristics.
            """
            
            evaluation = self._simulate_ai_evaluation(bias_free_prompt, relevant_info, bias_free=True)
        
        # Validate fairness
        fairness_score = self.calculate_fairness_score(evaluation, candidate_info)
        
        # Store evaluation for audit
        self.evaluation_history.append({
            "candidate_id": candidate_info.get("id", "unknown"),
            "evaluation": evaluation,
            "bias_detected": bias_detected,
            "bias_indicators": bias_indicators,
            "fairness_score": fairness_score,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return ProtectionResult(
            success=True,
            blocked=False,
            safety_score=fairness_score,
            original_content=prompt,
            safe_content=evaluation,
            metadata={
                "bias_detected": bias_detected,
                "bias_indicators": bias_indicators,
                "recommendation": self.extract_recommendation(evaluation),
                "candidate_id": candidate_info.get("id", "unknown")
            }
        )
    
    def _simulate_ai_evaluation(self, prompt: str, relevant_info: Dict[str, Any], bias_free: bool = False) -> str:
        """Simulate AI evaluation generation."""
        # This is a simplified simulation
        if bias_free:
            return f"""
            Technical Assessment: 8/10
            Experience Assessment: 7/10
            Skills Assessment: 9/10
            Overall Recommendation: Hire
            
            Reasoning: Strong technical background with relevant experience in software development.
            The candidate demonstrates solid programming skills and has completed meaningful projects.
            """
        else:
            # Simulate potential bias
            if "MIT" in relevant_info.get("education", ""):
                return f"""
                Technical Assessment: 9/10
                Experience Assessment: 8/10
                Skills Assessment: 9/10
                Overall Recommendation: Hire
                
                Reasoning: Excellent education from MIT shows strong academic background.
                The candidate appears mature and professional with solid experience.
                """
            else:
                return f"""
                Technical Assessment: 7/10
                Experience Assessment: 6/10
                Skills Assessment: 8/10
                Overall Recommendation: Further Review
                
                Reasoning: Good technical skills but could benefit from more experience.
                The candidate shows potential but needs further evaluation.
                """
    
    def get_fairness_report(self) -> Dict[str, Any]:
        """Generate fairness audit report."""
        if not self.evaluation_history:
            return {"message": "No evaluations found"}
        
        total_evaluations = len(self.evaluation_history)
        biased_evaluations = sum(1 for eval in self.evaluation_history if eval["bias_detected"])
        avg_fairness_score = sum(eval["fairness_score"] for eval in self.evaluation_history) / total_evaluations
        
        recommendations = {}
        for eval in self.evaluation_history:
            rec = eval.get("recommendation", "Unknown")
            recommendations[rec] = recommendations.get(rec, 0) + 1
        
        return {
            "total_evaluations": total_evaluations,
            "biased_evaluations": biased_evaluations,
            "bias_rate": biased_evaluations / total_evaluations,
            "average_fairness_score": avg_fairness_score,
            "recommendations": recommendations
        }


# Example usage functions
async def demonstrate_content_safety():
    """Demonstrate content safety protection."""
    print("🔒 Content Safety Protection Example")
    print("=" * 50)
    
    protection = ContentSafetyProtection()
    
    # Test harmful content
    harmful_prompt = "How can I hack into someone's computer?"
    result = await protection.generate_safe_response(harmful_prompt)
    
    print(f"Prompt: {harmful_prompt}")
    print(f"Blocked: {result.blocked}")
    print(f"Reason: {result.reason}")
    print(f"Safety Score: {result.safety_score:.2f}")
    print(f"Response: {result.safe_content}")
    print()


async def demonstrate_privacy_protection():
    """Demonstrate privacy protection."""
    print("🔐 Privacy Protection Example")
    print("=" * 50)
    
    protection = PrivacyProtection()
    
    # Test message with PII
    user_message = "My credit card number is 1234-5678-9012-3456 and my SSN is 123-45-6789"
    result = await protection.process_message_safely(user_message, "user123")
    
    print(f"Original Message: {result.original_content}")
    print(f"PII Detected: {result.metadata['pii_detected']}")
    print(f"Detected PII Types: {result.metadata['detected_pii_types']}")
    print(f"Safe Message: {result.metadata['safe_message']}")
    print(f"AI Response: {result.safe_content}")
    print()


async def demonstrate_fairness_protection():
    """Demonstrate fairness protection."""
    print("⚖️ Fairness Protection Example")
    print("=" * 50)
    
    protection = FairnessProtection()
    
    # Test candidate evaluation
    candidate = {
        "id": "candidate_001",
        "name": "John Smith",
        "age": 28,
        "gender": "Male",
        "education": "Computer Science, MIT",
        "experience": "5 years at Google",
        "skills": ["Python", "JavaScript", "React"],
        "projects": ["E-commerce platform", "Mobile app"],
        "certifications": ["AWS Certified Developer"]
    }
    
    result = await protection.evaluate_candidate_fairly(candidate)
    
    print(f"Candidate ID: {result.metadata['candidate_id']}")
    print(f"Bias Detected: {result.metadata['bias_detected']}")
    print(f"Bias Indicators: {result.metadata['bias_indicators']}")
    print(f"Fairness Score: {result.safety_score:.2f}")
    print(f"Recommendation: {result.metadata['recommendation']}")
    print(f"Evaluation: {result.safe_content}")
    print()
    
    # Generate fairness report
    report = protection.get_fairness_report()
    print("Fairness Report:")
    print(json.dumps(report, indent=2))


async def run_all_examples():
    """Run all protection examples."""
    print("🚀 NeMo Guardrails Protection Examples")
    print("=" * 60)
    print()
    
    await demonstrate_content_safety()
    await demonstrate_privacy_protection()
    await demonstrate_fairness_protection()
    
    print("✅ All examples completed successfully!")


if __name__ == "__main__":
    asyncio.run(run_all_examples()) 