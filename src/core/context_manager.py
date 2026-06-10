"""
Context Manager for maintaining conversation state and history.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path


class ContextManager:
    """Manages conversation context and history."""

    def __init__(self, config: Dict):
        """
        Initialize context manager.

        Args:
            config: Conversation configuration
        """
        self.config = config
        self.conversations = {}
        self.max_context_messages = config.get("max_context_messages", 20)
        self.enable_memory = config.get("enable_memory", True)
        self.retention_days = config.get("memory_retention_days", 90)

        # Ensure data directory exists
        self.data_dir = Path("data/conversations")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def create_conversation(
        self,
        customer_id: Optional[str] = None,
        channel: str = "chat",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Create a new conversation.

        Args:
            customer_id: Optional customer identifier
            channel: Communication channel
            metadata: Optional additional metadata

        Returns:
            Conversation ID
        """
        conversation_id = str(uuid.uuid4())

        conversation = {
            "id": conversation_id,
            "customer_id": customer_id,
            "channel": channel,
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": metadata or {},
            "status": "active"
        }

        self.conversations[conversation_id] = conversation

        # Load previous conversations for this customer if memory is enabled
        if self.enable_memory and customer_id:
            self._load_customer_history(conversation_id, customer_id)

        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """
        Add a message to a conversation.

        Args:
            conversation_id: Conversation identifier
            role: Message role (user/assistant)
            content: Message content
            metadata: Optional message metadata
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.conversations[conversation_id]["messages"].append(message)
        self.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()

        # Persist to disk
        self._save_conversation(conversation_id)

    def get_context(
        self,
        conversation_id: str,
        include_history: bool = True
    ) -> Dict:
        """
        Get conversation context.

        Args:
            conversation_id: Conversation identifier
            include_history: Whether to include customer history

        Returns:
            Context dictionary with messages and metadata
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        conversation = self.conversations[conversation_id]

        # Get recent messages (sliding window)
        messages = conversation["messages"][-self.max_context_messages:]

        context = {
            "conversation_id": conversation_id,
            "customer_id": conversation.get("customer_id"),
            "channel": conversation.get("channel"),
            "messages": messages,
            "metadata": conversation.get("metadata", {})
        }

        # Add customer history if available
        if include_history and self.enable_memory:
            context["customer_history"] = self._get_customer_summary(
                conversation.get("customer_id")
            )

        return context

    def update_metadata(
        self,
        conversation_id: str,
        key: str,
        value: Any
    ):
        """
        Update conversation metadata.

        Args:
            conversation_id: Conversation identifier
            key: Metadata key
            value: Metadata value
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        self.conversations[conversation_id]["metadata"][key] = value
        self._save_conversation(conversation_id)

    def end_conversation(
        self,
        conversation_id: str,
        status: str = "completed"
    ):
        """
        End a conversation.

        Args:
            conversation_id: Conversation identifier
            status: Final status (completed/escalated/abandoned)
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        self.conversations[conversation_id]["status"] = status
        self.conversations[conversation_id]["ended_at"] = datetime.now().isoformat()

        # Save final state
        self._save_conversation(conversation_id)

    def _load_customer_history(self, conversation_id: str, customer_id: str):
        """Load previous conversation history for a customer."""
        # Look for previous conversations from this customer
        history_summary = self._get_customer_summary(customer_id)

        if history_summary:
            self.conversations[conversation_id]["metadata"]["customer_history"] = \
                history_summary

    def _get_customer_summary(self, customer_id: Optional[str]) -> Optional[Dict]:
        """Get summary of previous conversations for a customer."""
        if not customer_id or not self.enable_memory:
            return None

        # Find all conversations for this customer
        customer_conversations = []

        for conv_file in self.data_dir.glob("*.json"):
            try:
                with open(conv_file, 'r') as f:
                    conv_data = json.load(f)

                if conv_data.get("customer_id") == customer_id:
                    # Check if within retention period
                    started_at = datetime.fromisoformat(
                        conv_data.get("started_at", datetime.now().isoformat())
                    )
                    if (datetime.now() - started_at).days <= self.retention_days:
                        customer_conversations.append(conv_data)
            except Exception:
                continue

        if not customer_conversations:
            return None

        # Build summary
        summary = {
            "total_conversations": len(customer_conversations),
            "recent_topics": self._extract_topics(customer_conversations),
            "common_issues": self._extract_issues(customer_conversations),
            "last_interaction": max(
                conv.get("updated_at", "") for conv in customer_conversations
            )
        }

        return summary

    def _extract_topics(self, conversations: List[Dict]) -> List[str]:
        """Extract common topics from conversations."""
        topics = set()

        for conv in conversations[-5:]:  # Last 5 conversations
            for message in conv.get("messages", []):
                content = message.get("content", "").lower()
                # Simple keyword extraction
                if "order" in content or "track" in content:
                    topics.add("orders")
                if "return" in content:
                    topics.add("returns")
                if "refund" in content:
                    topics.add("refunds")
                if "product" in content:
                    topics.add("products")

        return list(topics)

    def _extract_issues(self, conversations: List[Dict]) -> List[str]:
        """Extract common issues from conversations."""
        issues = []

        for conv in conversations[-5:]:
            status = conv.get("status", "")
            if status == "escalated":
                issues.append("required_escalation")
            metadata = conv.get("metadata", {})
            if metadata.get("failed_attempts", 0) > 0:
                issues.append("multiple_attempts")

        return list(set(issues))

    def _save_conversation(self, conversation_id: str):
        """Persist conversation to disk."""
        if conversation_id not in self.conversations:
            return

        conversation = self.conversations[conversation_id]
        file_path = self.data_dir / f"{conversation_id}.json"

        try:
            with open(file_path, 'w') as f:
                json.dump(conversation, f, indent=2)
        except Exception as e:
            print(f"Error saving conversation: {e}")

    def cleanup_old_conversations(self):
        """Remove conversations older than retention period."""
        if not self.enable_memory:
            return

        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        for conv_file in self.data_dir.glob("*.json"):
            try:
                with open(conv_file, 'r') as f:
                    conv_data = json.load(f)

                started_at = datetime.fromisoformat(
                    conv_data.get("started_at", datetime.now().isoformat())
                )

                if started_at < cutoff_date:
                    conv_file.unlink()

                    # Remove from memory if loaded
                    conv_id = conv_data.get("id")
                    if conv_id in self.conversations:
                        del self.conversations[conv_id]

            except Exception as e:
                print(f"Error cleaning up {conv_file}: {e}")
