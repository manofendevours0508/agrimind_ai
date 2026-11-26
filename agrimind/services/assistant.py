from agrimind.services.ai_provider import AIProvider


class AssistantService:
    """Coordinates agricultural questions with an AI provider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def ask(self, prompt: str) -> str:
        """Send a question to the configured AI provider."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")

        return self.provider.generate_response(prompt.strip())
