from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Common interface for all AgriMind AI providers."""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate an answer from a user's prompt."""
        raise NotImplementedError


class AIProviderError(Exception):
    """Raised when an AI provider cannot generate a response."""
