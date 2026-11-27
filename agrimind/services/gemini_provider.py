import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from agrimind.services.ai_provider import AIProvider, AIProviderError


class GeminiProvider(AIProvider):
    """Connect to Gemini using Python's built-in HTTP client."""

    def __init__(self, model="gemini-3.5-flash-lite", timeout=30):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model = model
        self.timeout = timeout

        if not self.api_key:
            raise AIProviderError("GEMINI_API_KEY is not configured.")

    def generate_response(self, prompt: str) -> str:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as error:
            raise AIProviderError("Gemini request failed.") from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise AIProviderError("Gemini returned an invalid response.") from error

        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as error:
            raise AIProviderError("Gemini response did not contain text.") from error
