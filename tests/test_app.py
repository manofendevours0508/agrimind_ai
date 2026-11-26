import pytest

from agrimind import create_app
from agrimind.config import DevelopmentConfig, ProductionConfig, TestingConfig


class TestConfig:
    TESTING = True
    DEBUG = False
    SECRET_KEY = "test-only"


class ErrorTestConfig(TestConfig):
    TESTING = False


def test_create_app_registers_routes():
    app = create_app(TestConfig)

    assert app.test_client().get("/").status_code == 200
    assert app.test_client().get("/api/health").status_code == 200


def test_health_check_returns_json():
    response = create_app(TestConfig).test_client().get("/api/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "ok", "service": "AgriMind AI"}


def test_landing_page_is_available():
    response = create_app(TestConfig).test_client().get("/")

    assert response.status_code == 200
    assert b"AgriMind AI" in response.data
    assert b"agricultural" in response.data.lower()


def test_missing_api_route_returns_json_404():
    response = create_app(TestConfig).test_client().get("/api/not-a-route")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "Not Found"


def test_missing_page_returns_branded_404():
    response = create_app(TestConfig).test_client().get("/not-a-page")

    assert response.status_code == 404
    assert b"Page not found" in response.data


def test_internal_api_error_does_not_expose_exception_details():
    app = create_app(ErrorTestConfig)

    @app.get("/api/failure")
    def fail():
        raise RuntimeError("sensitive diagnostic detail")

    response = app.test_client().get("/api/failure")

    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal Server Error"}
    assert b"sensitive diagnostic detail" not in response.data


def test_development_config_is_selected_by_default():
    app = create_app()

    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is False


def test_testing_config_can_be_selected():
    app = create_app(TestingConfig)

    assert app.config["DEBUG"] is False
    assert app.config["TESTING"] is True


def test_production_rejects_missing_secret(monkeypatch):
    monkeypatch.setattr(ProductionConfig, "SECRET_KEY", None)

    with pytest.raises(RuntimeError, match="AGRIMIND_SECRET_KEY"):
        create_app(ProductionConfig)


def test_production_accepts_configured_secret(monkeypatch):
    secret = "safe-test-secret-key-with-more-than-32-characters"
    monkeypatch.setattr(ProductionConfig, "SECRET_KEY", secret)

    app = create_app(ProductionConfig)

    assert app.config["SECRET_KEY"] == secret
    assert app.config["DEBUG"] is False


def test_production_rejects_short_secret(monkeypatch):
    monkeypatch.setattr(ProductionConfig, "SECRET_KEY", "weak-secret")

    with pytest.raises(RuntimeError, match="at least 32 characters"):
        create_app(ProductionConfig)


def test_landing_page_shows_planned_capabilities():
    response = create_app(TestConfig).test_client().get("/")

    assert response.status_code == 200
    assert b"Agricultural knowledge" in response.data
    assert b"Dataset exploration" in response.data
    assert b"Evidence-led insights" in response.data
    assert b"Planned capability" in response.data


def test_mobile_navigation_has_accessibility_attributes():
    response = create_app(TestConfig).test_client().get("/")

    assert b'class="menu-toggle"' in response.data
    assert b'aria-expanded="false"' in response.data
    assert b'aria-controls="primary-nav"' in response.data
    assert b'id="primary-nav"' in response.data


def test_frontend_assets_are_available():
    client = create_app(TestConfig).test_client()

    css_response = client.get("/static/css/styles.css")
    js_response = client.get("/static/js/main.js")

    assert css_response.status_code == 200
    assert js_response.status_code == 200
    assert b"capability-grid" in css_response.data
    assert b"event.key === \"Escape\"" in js_response.data
