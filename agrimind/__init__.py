from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException, InternalServerError

from agrimind.config import DevelopmentConfig


def create_app(config_object=DevelopmentConfig):
    """Create and configure an AgriMind AI Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    from agrimind.routes.api import api_bp
    from agrimind.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        if request.path.startswith("/api"):
            return jsonify(error=error.name, message=error.description), error.code
        if error.code == 404:
            return render_template("404.html"), error.code
        return error

    @app.errorhandler(InternalServerError)
    def handle_internal_error(error):
        app.logger.error("Unhandled application error", exc_info=error.original_exception)
        if request.path.startswith("/api"):
            return jsonify(error="Internal Server Error"), 500
        return render_template("500.html"), 500

    return app
