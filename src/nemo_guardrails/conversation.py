"""
Conversation management for Nvidia NeMo Guardrails.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from .models import Message, SafetyResult


class ConversationManager:
    """Manages conversation flow and context."""
    
    def __init__(self, max_history: int = 100):
        """
        Initialize conversation manager.
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.max_history = max_history
        self.conversations: Dict[str, List[Message]] = {}
        
    async def add_message(self, message: Message, session_id: Optional[str] = None) -> str:
        """
        Add a message to the conversation history.
        
        Args:
            message: Message object to add
            session_id: Session identifier (generated if not provided)
            
        Returns:
            Session ID for the conversation
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
            
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            
        # Generate message ID if not provided
        if message.message_id is None:
            message.message_id = str(uuid.uuid4())
            
        self.conversations[session_id].append(message)
        
        # Maintain max history
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]
            
        return session_id
    
    async def get_context(self, session_id: str, window: int = 10) -> List[Message]:
        """
        Get recent conversation context.
        
        Args:
            session_id: Session identifier
            window: Number of recent messages to include
            
        Returns:
            List of recent messages
        """
        if session_id not in self.conversations:
            return []
            
        messages = self.conversations[session_id]
        return messages[-window:] if len(messages) > window else messages
    
    async def get_full_history(self, session_id: str) -> List[Message]:
        """
        Get full conversation history.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of all messages in the conversation
        """
        return self.conversations.get(session_id, [])
    
    async def check_conversation_safety(self, session_id: str) -> SafetyResult:
        """
        Check the entire conversation for safety violations.
        
        Args:
            session_id: Session identifier
            
        Returns:
            SafetyResult for the conversation
        """
        messages = await self.get_full_history(session_id)
        
        if not messages:
            return SafetyResult(
                safe=True,
                score=1.0,
                violations=[],
                timestamp=datetime.utcnow()
            )
        
        # Combine all message content
        full_content = "\n".join([msg.content for msg in messages])
        
        # This would integrate with the GuardrailsEngine
        # For now, return a basic safety check
        violations = []
        score = 1.0
        
        # Simple check for potentially harmful patterns
        harmful_patterns = ["harmful", "dangerous", "illegal"]
        content_lower = full_content.lower()
        
        for pattern in harmful_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "severity": "medium"
                })
                score *= 0.8
        
        return SafetyResult(
            safe=score >= 0.8 and len(violations) == 0,
            score=score,
            violations=violations,
            timestamp=datetime.utcnow(),
            metadata={"session_id": session_id, "message_count": len(messages)}
        )
    
    async def clear_conversation(self, session_id: str) -> bool:
        """
        Clear a conversation's history.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if conversation was cleared, False if not found
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
            return True
        return False
    
    async def get_conversation_stats(self, session_id: str) -> Dict[str, Any]:
        """
        Get statistics about a conversation.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with conversation statistics
        """
        messages = await self.get_full_history(session_id)
        
        if not messages:
            return {
                "session_id": session_id,
                "message_count": 0,
                "duration": 0,
                "users": set(),
                "start_time": None,
                "end_time": None
            }
        
        start_time = min(msg.timestamp for msg in messages)
        end_time = max(msg.timestamp for msg in messages)
        duration = (end_time - start_time).total_seconds()
        users = set(msg.user_id for msg in messages)
        
        return {
            "session_id": session_id,
            "message_count": len(messages),
            "duration": duration,
            "users": list(users),
            "start_time": start_time,
            "end_time": end_time
        }
    
    async def list_conversations(self) -> List[str]:
        """
        List all active conversation session IDs.
        
        Returns:
            List of session IDs
        """
        return list(self.conversations.keys()) 