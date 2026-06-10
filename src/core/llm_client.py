"""
LLM Client for interacting with Claude API with prompt caching support.
"""

import os
import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic


class LLMClient:
    """Client for interacting with Claude API with caching and optimization."""

    def __init__(self, config: Dict):
        """
        Initialize LLM client with configuration.

        Args:
            config: LLM configuration dictionary
        """
        self.config = config
        api_key = config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in config or environment")

        self.client = Anthropic(api_key=api_key)
        self.model = config.get("model", "claude-sonnet-4-6")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.7)
        self.enable_caching = config.get("enable_caching", True)
        self.streaming = config.get("streaming", False)
        self.thinking_enabled = config.get("thinking", {}).get("enabled", True)

    def create_message(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        enable_thinking: bool = None
    ) -> Dict[str, Any]:
        """
        Create a message using Claude API with optional caching.

        Args:
            messages: List of message dictionaries
            system: System prompt
            tools: Optional tool definitions
            max_tokens: Override max tokens
            temperature: Override temperature
            enable_thinking: Override thinking setting

        Returns:
            Response dictionary from Claude
        """
        # Prepare system prompt with caching
        system_blocks = []
        if system:
            if self.enable_caching:
                # Cache system prompt for efficiency
                system_blocks = [
                    {
                        "type": "text",
                        "text": system,
                        "cache_control": {"type": "ephemeral"}
                    }
                ]
            else:
                system_blocks = [{"type": "text", "text": system}]

        # Prepare request parameters
        request_params = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "messages": messages
        }

        if system_blocks:
            request_params["system"] = system_blocks

        if tools:
            request_params["tools"] = tools

        # Add thinking/extended thinking
        if enable_thinking is None:
            enable_thinking = self.thinking_enabled

        if enable_thinking:
            thinking_type = self.config.get("thinking", {}).get("type", "enabled")
            request_params["thinking"] = {"type": thinking_type}

        try:
            # Make API call
            response = self.client.messages.create(**request_params)

            # Parse response
            result = {
                "id": response.id,
                "model": response.model,
                "role": response.role,
                "content": [],
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }

            # Extract thinking and text content
            thinking_content = []
            text_content = []

            for block in response.content:
                if block.type == "thinking":
                    thinking_content.append(block.thinking)
                elif block.type == "text":
                    text_content.append(block.text)
                elif block.type == "tool_use":
                    result["content"].append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input
                    })

            # Add thinking and text to result
            if thinking_content:
                result["thinking"] = "\n".join(thinking_content)

            if text_content:
                result["text"] = "\n".join(text_content)
                result["content"].append({
                    "type": "text",
                    "text": result["text"]
                })

            # Add cache metrics if available
            if hasattr(response.usage, "cache_creation_input_tokens"):
                result["usage"]["cache_creation_input_tokens"] = \
                    response.usage.cache_creation_input_tokens
            if hasattr(response.usage, "cache_read_input_tokens"):
                result["usage"]["cache_read_input_tokens"] = \
                    response.usage.cache_read_input_tokens

            return result

        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")

    def create_message_stream(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ):
        """
        Create a streaming message using Claude API.

        Args:
            messages: List of message dictionaries
            system: System prompt
            tools: Optional tool definitions
            max_tokens: Override max tokens
            temperature: Override temperature

        Yields:
            Response chunks from Claude
        """
        request_params = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "messages": messages,
            "stream": True
        }

        if system:
            request_params["system"] = system

        if tools:
            request_params["tools"] = tools

        try:
            with self.client.messages.stream(**request_params) as stream:
                for chunk in stream:
                    yield chunk
        except Exception as e:
            raise Exception(f"LLM streaming error: {str(e)}")

    def extract_text(self, response: Dict) -> str:
        """
        Extract text content from response.

        Args:
            response: Response dictionary from create_message

        Returns:
            Extracted text
        """
        return response.get("text", "")

    def extract_thinking(self, response: Dict) -> Optional[str]:
        """
        Extract thinking content from response.

        Args:
            response: Response dictionary from create_message

        Returns:
            Extracted thinking or None
        """
        return response.get("thinking")

    def extract_tool_uses(self, response: Dict) -> List[Dict]:
        """
        Extract tool use blocks from response.

        Args:
            response: Response dictionary from create_message

        Returns:
            List of tool use dictionaries
        """
        tool_uses = []
        for block in response.get("content", []):
            if block.get("type") == "tool_use":
                tool_uses.append(block)
        return tool_uses
