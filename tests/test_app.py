from agrimind import create_app


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
