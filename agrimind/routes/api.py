from flask import Blueprint, current_app, jsonify, request

from agrimind.services.ai_provider import AIProviderError

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify(status="ok", service="AgriMind AI")


@api_bp.post("/chat")
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Request body must be valid JSON."), 400

    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify(error="A non-empty message is required."), 400

    if len(message) > 2000:
        return jsonify(error="Message must not exceed 2000 characters."), 400

    assistant = current_app.extensions.get("assistant_service")

    if assistant is None:
        return jsonify(error="AI assistant is not configured yet."), 503

    try:
        response = assistant.ask(message)
    except AIProviderError:
        current_app.logger.exception("AI provider request failed")
        return jsonify(error="AI provider is temporarily unavailable."), 503

    return jsonify(response=response)
