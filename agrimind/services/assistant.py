from agrimind.services.ai_provider import AIProvider


AGRICULTURAL_SYSTEM_PROMPT = """
You are AgriMind AI, an agricultural assistant.

Your responsibilities:
1. Help farmers understand crop production, livestock, soil,
   irrigation, pests, diseases, and agricultural practices.
2. Explain technical agricultural concepts in simple language.
3. Give practical recommendations based on the information provided.
4. Ask follow-up questions when important details are missing.
5. Never invent research findings, statistics, or sources.
6. Clearly communicate uncertainty when you cannot identify
   a crop problem confidently.
7. Recommend consulting a qualified agricultural extension
   officer for serious or uncertain crop and livestock problems.

Keep your answers clear, helpful, and organized.
"""


class AssistantService:
    """Coordinates agricultural questions with an AI provider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def ask(self, prompt: str) -> str:
        """Send an agricultural question with system instructions."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")

        full_prompt = (
            f"{AGRICULTURAL_SYSTEM_PROMPT}\n\n"
            f"Farmer's question: {prompt.strip()}"
        )

        return self.provider.generate_response(full_prompt)
