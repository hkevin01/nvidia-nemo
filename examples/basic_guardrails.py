#!/usr/bin/env python3
"""
Basic example demonstrating Nvidia NeMo Guardrails usage.

This example shows how to:
1. Initialize the guardrails engine
2. Check content safety
3. Validate AI outputs
4. Manage conversations
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nemo_guardrails import (
    GuardrailsEngine,
    ConversationManager,
    ConfigManager,
    Message,
    Rule
)


async def main():
    """Main example function."""
    print("🚀 Nvidia NeMo Guardrails - Basic Example")
    print("=" * 50)
    
    # Initialize components
    print("\n1. Initializing components...")
    engine = GuardrailsEngine()
    conversation_manager = ConversationManager()
    config_manager = ConfigManager()
    
    # Load configuration
    await config_manager.load_config()
    print(f"   ✅ Loaded {len(config_manager.get_rules())} rules")
    
    # Initialize engine with rules
    engine.rules = config_manager.get_enabled_rules()
    await engine.initialize()
    print("   ✅ Engine initialized")
    
    # Example 1: Content Safety Check
    print("\n2. Content Safety Check")
    print("-" * 30)
    
    test_content = "Hello, this is a safe message for testing."
    print(f"   Testing content: '{test_content}'")
    
    safety_result = await engine.check_content(test_content)
    print(f"   ✅ Safe: {safety_result.safe}")
    print(f"   📊 Score: {safety_result.score:.2f}")
    print(f"   ⚠️  Violations: {len(safety_result.violations)}")
    
    # Example 2: Unsafe Content Check
    print("\n3. Unsafe Content Check")
    print("-" * 30)
    
    unsafe_content = "This message contains harmful content that should be flagged."
    print(f"   Testing content: '{unsafe_content}'")
    
    safety_result = await engine.check_content(unsafe_content)
    print(f"   ✅ Safe: {safety_result.safe}")
    print(f"   📊 Score: {safety_result.score:.2f}")
    print(f"   ⚠️  Violations: {len(safety_result.violations)}")
    
    if safety_result.violations:
        for violation in safety_result.violations:
            print(f"      - {violation.description} (severity: {violation.severity})")
    
    # Example 3: Output Validation
    print("\n4. AI Output Validation")
    print("-" * 30)
    
    ai_output = "Here is a helpful response to your question about machine learning."
    print(f"   Testing AI output: '{ai_output}'")
    
    validation_result = await engine.validate_output(ai_output)
    print(f"   ✅ Valid: {validation_result.valid}")
    print(f"   ⚠️  Issues: {len(validation_result.issues)}")
    print(f"   💡 Suggestions: {len(validation_result.suggestions)}")
    
    if validation_result.issues:
        for issue in validation_result.issues:
            print(f"      - Issue: {issue}")
    
    if validation_result.suggestions:
        for suggestion in validation_result.suggestions:
            print(f"      - Suggestion: {suggestion}")
    
    # Example 4: Conversation Management
    print("\n5. Conversation Management")
    print("-" * 30)
    
    # Create a conversation
    session_id = await conversation_manager.add_message(
        Message("Hello, how are you?", "user123")
    )
    print(f"   ✅ Created conversation: {session_id}")
    
    # Add more messages
    await conversation_manager.add_message(
        Message("I'm doing well, thank you!", "bot"),
        session_id
    )
    await conversation_manager.add_message(
        Message("That's great to hear!", "user123"),
        session_id
    )
    
    # Get conversation context
    context = await conversation_manager.get_context(session_id)
    print(f"   📝 Conversation has {len(context)} messages")
    
    # Check conversation safety
    conversation_safety = await conversation_manager.check_conversation_safety(session_id)
    print(f"   ✅ Conversation safe: {conversation_safety.safe}")
    print(f"   📊 Safety score: {conversation_safety.score:.2f}")
    
    # Get conversation stats
    stats = await conversation_manager.get_conversation_stats(session_id)
    print(f"   📊 Stats: {stats['message_count']} messages, {stats['duration']:.1f}s duration")
    
    # Example 5: Custom Rules
    print("\n6. Custom Rules")
    print("-" * 30)
    
    # Create a custom rule
    custom_rule = Rule(
        name="custom_keyword_check",
        description="Check for specific keywords",
        enabled=True,
        threshold=0.9,
        parameters={"keywords": ["spam", "advertisement", "promotion"]}
    )
    
    config_manager.add_rule(custom_rule)
    print(f"   ✅ Added custom rule: {custom_rule.name}")
    
    # Test with custom rule
    test_with_custom = "This is a promotional message with advertisement content."
    print(f"   Testing with custom rule: '{test_with_custom}'")
    
    # Update engine with new rules
    engine.rules = config_manager.get_enabled_rules()
    safety_result = await engine.check_content(test_with_custom)
    print(f"   ✅ Safe: {safety_result.safe}")
    print(f"   📊 Score: {safety_result.score:.2f}")
    
    print("\n🎉 Example completed successfully!")
    print("\nNext steps:")
    print("1. Explore the API documentation in docs/api-reference.md")
    print("2. Check out more examples in the examples/ directory")
    print("3. Read the project plan in docs/project-plan.md")
    print("4. Contribute to the project following docs/contributing.md")


if __name__ == "__main__":
    asyncio.run(main()) 