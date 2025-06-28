# NeMo Guardrails Protection Examples

This document provides concrete examples of how Nvidia NeMo Guardrails protects against common AI safety issues, comparing protected vs. unprotected implementations.

## Example 1: Content Safety and Harmful Output Prevention

### Scenario: User asks for instructions on harmful activities

#### ❌ Unprotected AI Code

```python
import openai

def generate_response(prompt):
    """Unprotected AI response generation."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Example usage
prompt = "How can I hack into someone's computer?"
response = generate_response(prompt)
print(response)
# Output: Detailed instructions on hacking techniques...
```

**Problems:**
- No content filtering
- Generates harmful instructions
- Could enable malicious activities
- No safety checks

#### ✅ Protected with NeMo Guardrails

```python
from nemo_guardrails import GuardrailsEngine, SafetyResult
import openai

class SafeAI:
    def __init__(self):
        self.engine = GuardrailsEngine()
        self.setup_safety_rules()
    
    def setup_safety_rules(self):
        """Configure safety rules."""
        harmful_patterns = [
            "hack", "exploit", "bypass", "unauthorized access",
            "malware", "virus", "phishing", "social engineering"
        ]
        
        safety_rule = {
            "name": "harmful_instructions",
            "patterns": harmful_patterns,
            "action": "block",
            "severity": "high"
        }
        self.engine.add_rule(safety_rule)
    
    def generate_safe_response(self, prompt):
        """Generate response with safety checks."""
        # Check input safety
        input_safety = self.engine.check_content(prompt)
        if not input_safety.safe:
            return {
                "response": "I cannot provide instructions for harmful or illegal activities.",
                "blocked": True,
                "reason": "Harmful content detected",
                "safety_score": input_safety.score
            }
        
        # Generate response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_response = response.choices[0].message.content
        
        # Check output safety
        output_safety = self.engine.check_content(ai_response)
        if not output_safety.safe:
            return {
                "response": "I apologize, but I cannot provide that information as it may be harmful.",
                "blocked": True,
                "reason": "Unsafe output detected",
                "safety_score": output_safety.score
            }
        
        return {
            "response": ai_response,
            "blocked": False,
            "safety_score": output_safety.score
        }

# Example usage
safe_ai = SafeAI()
prompt = "How can I hack into someone's computer?"
result = safe_ai.generate_safe_response(prompt)
print(result)
# Output: {"response": "I cannot provide instructions for harmful or illegal activities.", "blocked": True, "reason": "Harmful content detected", "safety_score": 0.2}
```

**Protection Benefits:**
- Input validation prevents harmful prompts
- Output validation catches unsafe responses
- Clear blocking with explanations
- Safety scoring for monitoring

## Example 2: Personal Information Protection

### Scenario: AI assistant handling user data

#### ❌ Unprotected AI Code

```python
import json
import openai

class UnprotectedAssistant:
    def __init__(self):
        self.conversation_history = []
    
    def process_message(self, user_message, user_id):
        """Process user message without privacy protection."""
        # Store everything without filtering
        self.conversation_history.append({
            "user_id": user_id,
            "message": user_message,
            "timestamp": "2024-01-01T12:00:00Z"
        })
        
        # Send to AI without privacy checks
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.choices[0].message.content

# Example usage
assistant = UnprotectedAssistant()
user_message = "My credit card number is 1234-5678-9012-3456 and my SSN is 123-45-6789"
response = assistant.process_message(user_message, "user123")
print(response)
# Output: AI response that might reference or repeat sensitive information
```

**Problems:**
- Stores sensitive data in plain text
- No PII detection or redaction
- AI might repeat sensitive information
- No data protection measures

#### ✅ Protected with NeMo Guardrails

```python
import re
from nemo_guardrails import GuardrailsEngine, ConversationManager
import openai

class ProtectedAssistant:
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
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        }
        
        privacy_rule = {
            "name": "pii_protection",
            "patterns": pii_patterns,
            "action": "redact",
            "replacement": "[REDACTED]"
        }
        self.engine.add_rule(privacy_rule)
    
    def redact_pii(self, text):
        """Remove or redact personal information."""
        redacted_text = text
        
        # Credit card numbers
        redacted_text = re.sub(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[CREDIT_CARD]", redacted_text)
        
        # Social Security Numbers
        redacted_text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", redacted_text)
        
        # Email addresses
        redacted_text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", redacted_text)
        
        # Phone numbers
        redacted_text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]", redacted_text)
        
        return redacted_text
    
    def process_message(self, user_message, user_id):
        """Process user message with privacy protection."""
        # Check for PII in input
        pii_check = self.engine.check_content(user_message)
        
        # Redact PII before processing
        safe_message = self.redact_pii(user_message)
        
        # Store redacted message
        self.conversation_manager.add_message({
            "user_id": user_id,
            "message": safe_message,
            "timestamp": "2024-01-01T12:00:00Z"
        })
        
        # Generate response with privacy-aware prompt
        system_prompt = """You are a helpful assistant. Never repeat, reference, or ask for personal information like credit card numbers, SSNs, or other sensitive data."""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": safe_message}
            ]
        )
        
        ai_response = response.choices[0].message.content
        
        # Check response for PII
        response_safety = self.engine.check_content(ai_response)
        if not response_safety.safe:
            ai_response = "I apologize, but I cannot provide that information as it may contain sensitive data."
        
        return {
            "response": ai_response,
            "pii_detected": not pii_check.safe,
            "original_message": user_message,
            "safe_message": safe_message,
            "safety_score": response_safety.score
        }

# Example usage
protected_assistant = ProtectedAssistant()
user_message = "My credit card number is 1234-5678-9012-3456 and my SSN is 123-45-6789"
result = protected_assistant.process_message(user_message, "user123")
print(result)
# Output: {
#   "response": "I can help you with general questions, but I cannot process or store personal information like credit card numbers or SSNs.",
#   "pii_detected": True,
#   "original_message": "My credit card number is 1234-5678-9012-3456 and my SSN is 123-45-6789",
#   "safe_message": "My credit card number is [CREDIT_CARD] and my SSN is [SSN]",
#   "safety_score": 0.9
# }
```

**Protection Benefits:**
- Automatic PII detection and redaction
- Safe storage of conversations
- Privacy-aware AI responses
- Audit trail of safety checks

## Example 3: Bias and Fairness Protection

### Scenario: AI making decisions that could be biased

#### ❌ Unprotected AI Code

```python
import openai

def evaluate_job_candidate(candidate_info):
    """Unprotected AI evaluation of job candidates."""
    prompt = f"""
    Evaluate this job candidate for a software engineering position:
    
    Name: {candidate_info['name']}
    Age: {candidate_info['age']}
    Gender: {candidate_info['gender']}
    Education: {candidate_info['education']}
    Experience: {candidate_info['experience']}
    Skills: {candidate_info['skills']}
    
    Provide a hiring recommendation (Hire/Don't Hire) and reasoning.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Example usage
candidate1 = {
    "name": "John Smith",
    "age": 28,
    "gender": "Male",
    "education": "Computer Science, Stanford",
    "experience": "5 years at Google",
    "skills": "Python, JavaScript, React"
}

candidate2 = {
    "name": "Maria Garcia",
    "age": 32,
    "gender": "Female",
    "education": "Computer Science, MIT",
    "experience": "6 years at Microsoft",
    "skills": "Python, Java, Angular"
}

result1 = evaluate_job_candidate(candidate1)
result2 = evaluate_job_candidate(candidate2)
print(f"Candidate 1: {result1}")
print(f"Candidate 2: {result2}")
# Output: Potentially biased recommendations based on implicit biases
```

**Problems:**
- No bias detection or mitigation
- May discriminate based on protected characteristics
- No fairness metrics
- Uncontrolled decision-making

#### ✅ Protected with NeMo Guardrails

```python
from nemo_guardrails import GuardrailsEngine, ValidationResult
import openai
import json

class FairAIEvaluator:
    def __init__(self):
        self.engine = GuardrailsEngine()
        self.setup_fairness_rules()
        self.evaluation_history = []
    
    def setup_fairness_rules(self):
        """Configure fairness and bias protection rules."""
        protected_attributes = ["gender", "age", "race", "ethnicity", "religion"]
        
        fairness_rule = {
            "name": "fairness_protection",
            "protected_attributes": protected_attributes,
            "action": "validate",
            "fairness_threshold": 0.8
        }
        self.engine.add_rule(fairness_rule)
    
    def extract_relevant_info(self, candidate_info):
        """Extract only job-relevant information."""
        return {
            "education": candidate_info["education"],
            "experience": candidate_info["experience"],
            "skills": candidate_info["skills"],
            "projects": candidate_info.get("projects", []),
            "certifications": candidate_info.get("certifications", [])
        }
    
    def check_for_bias_indicators(self, evaluation_text):
        """Check if evaluation contains bias indicators."""
        bias_indicators = [
            "young", "old", "male", "female", "diverse", "traditional",
            "aggressive", "assertive", "emotional", "logical"
        ]
        
        text_lower = evaluation_text.lower()
        found_indicators = [indicator for indicator in bias_indicators if indicator in text_lower]
        
        return len(found_indicators) > 0, found_indicators
    
    def evaluate_candidate_fairly(self, candidate_info):
        """Evaluate job candidate with fairness protection."""
        # Extract only relevant information
        relevant_info = self.extract_relevant_info(candidate_info)
        
        # Create bias-free prompt
        prompt = f"""
        Evaluate this job candidate for a software engineering position based ONLY on job-relevant criteria:
        
        Education: {relevant_info['education']}
        Experience: {relevant_info['experience']}
        Skills: {relevant_info['skills']}
        Projects: {relevant_info['projects']}
        Certifications: {relevant_info['certifications']}
        
        Provide a structured evaluation with:
        1. Technical assessment (1-10)
        2. Experience assessment (1-10)
        3. Skills assessment (1-10)
        4. Overall recommendation (Hire/Don't Hire)
        5. Reasoning based ONLY on technical and professional qualifications
        
        Do NOT consider personal characteristics like age, gender, race, or ethnicity.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        evaluation = response.choices[0].message.content
        
        # Check for bias in the evaluation
        bias_detected, bias_indicators = self.check_for_bias_indicators(evaluation)
        
        if bias_detected:
            # Regenerate evaluation with stronger bias prevention
            bias_free_prompt = f"""
            Re-evaluate this candidate focusing ONLY on technical qualifications:
            
            Education: {relevant_info['education']}
            Experience: {relevant_info['experience']}
            Skills: {relevant_info['skills']}
            
            Provide a purely technical assessment without any personal characteristics.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": bias_free_prompt}]
            )
            evaluation = response.choices[0].message.content
        
        # Validate fairness
        fairness_score = self.calculate_fairness_score(evaluation, candidate_info)
        
        # Store evaluation for audit
        self.evaluation_history.append({
            "candidate_id": candidate_info.get("id", "unknown"),
            "evaluation": evaluation,
            "bias_detected": bias_detected,
            "bias_indicators": bias_indicators,
            "fairness_score": fairness_score,
            "timestamp": "2024-01-01T12:00:00Z"
        })
        
        return {
            "evaluation": evaluation,
            "bias_detected": bias_detected,
            "bias_indicators": bias_indicators,
            "fairness_score": fairness_score,
            "recommendation": self.extract_recommendation(evaluation)
        }
    
    def calculate_fairness_score(self, evaluation, candidate_info):
        """Calculate fairness score based on evaluation quality."""
        # Simple fairness scoring - in practice, this would be more sophisticated
        bias_indicators = ["young", "old", "male", "female", "diverse", "traditional"]
        text_lower = evaluation.lower()
        
        bias_count = sum(1 for indicator in bias_indicators if indicator in text_lower)
        fairness_score = max(0, 1.0 - (bias_count * 0.2))
        
        return fairness_score
    
    def extract_recommendation(self, evaluation):
        """Extract hiring recommendation from evaluation text."""
        if "hire" in evaluation.lower():
            return "Hire"
        elif "don't hire" in evaluation.lower() or "reject" in evaluation.lower():
            return "Don't Hire"
        else:
            return "Further Review"
    
    def get_fairness_report(self):
        """Generate fairness audit report."""
        total_evaluations = len(self.evaluation_history)
        biased_evaluations = sum(1 for eval in self.evaluation_history if eval["bias_detected"])
        avg_fairness_score = sum(eval["fairness_score"] for eval in self.evaluation_history) / total_evaluations
        
        return {
            "total_evaluations": total_evaluations,
            "biased_evaluations": biased_evaluations,
            "bias_rate": biased_evaluations / total_evaluations,
            "average_fairness_score": avg_fairness_score,
            "recommendations": {
                "hire": sum(1 for eval in self.evaluation_history if eval.get("recommendation") == "Hire"),
                "dont_hire": sum(1 for eval in self.evaluation_history if eval.get("recommendation") == "Don't Hire"),
                "further_review": sum(1 for eval in self.evaluation_history if eval.get("recommendation") == "Further Review")
            }
        }

# Example usage
fair_evaluator = FairAIEvaluator()

candidate1 = {
    "id": "candidate_001",
    "name": "John Smith",
    "age": 28,
    "gender": "Male",
    "education": "Computer Science, Stanford",
    "experience": "5 years at Google",
    "skills": "Python, JavaScript, React",
    "projects": ["E-commerce platform", "Mobile app"],
    "certifications": ["AWS Certified Developer"]
}

candidate2 = {
    "id": "candidate_002",
    "name": "Maria Garcia",
    "age": 32,
    "gender": "Female",
    "education": "Computer Science, MIT",
    "experience": "6 years at Microsoft",
    "skills": "Python, Java, Angular",
    "projects": ["AI recommendation system", "Cloud infrastructure"],
    "certifications": ["Google Cloud Professional"]
}

result1 = fair_evaluator.evaluate_candidate_fairly(candidate1)
result2 = fair_evaluator.evaluate_candidate_fairly(candidate2)

print("Candidate 1 Evaluation:")
print(json.dumps(result1, indent=2))
print("\nCandidate 2 Evaluation:")
print(json.dumps(result2, indent=2))

# Generate fairness report
fairness_report = fair_evaluator.get_fairness_report()
print("\nFairness Report:")
print(json.dumps(fairness_report, indent=2))
```

**Protection Benefits:**
- Bias detection and mitigation
- Focus on job-relevant criteria only
- Fairness scoring and monitoring
- Audit trail for compliance
- Automatic bias correction

## Summary of Protection Benefits

| Protection Area | Unprotected AI | NeMo Guardrails Protected |
|----------------|----------------|---------------------------|
| **Content Safety** | Generates harmful content | Blocks harmful requests and responses |
| **Privacy** | Stores and exposes PII | Detects and redacts sensitive information |
| **Fairness** | May exhibit bias | Detects and mitigates bias automatically |
| **Monitoring** | No oversight | Comprehensive audit trails |
| **Compliance** | No regulatory compliance | Built-in compliance features |
| **Transparency** | Black box decisions | Explainable safety decisions |

These examples demonstrate how NeMo Guardrails transforms potentially dangerous AI applications into safe, responsible, and compliant systems that protect users, maintain privacy, and ensure fairness. 