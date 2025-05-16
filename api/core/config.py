import os

APP_ENV = os.getenv("APP_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "Fastapi ft MongoDB Sample Project")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "---")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

ROUTE_PREFIX = os.getenv("ROUTE_PREFIX", "api/v1")

# MongoDB config
DATABASE_NAME = os.getenv("DATABASE_NAME", "testDB")
DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://localhost:27017")
