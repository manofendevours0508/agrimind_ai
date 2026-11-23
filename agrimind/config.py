import os


class DevelopmentConfig:
    """Local development settings; production settings will be added later."""

    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("AGRIMIND_SECRET_KEY")
