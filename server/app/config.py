"""
Application configuration and settings
"""
import os
from typing import Optional

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API Configuration
API_TITLE = "Todo API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "A modern REST API for managing todos"

# Database Configuration
USE_POSTGRESQL = os.getenv("USE_POSTGRESQL", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL")

if USE_POSTGRESQL:
    if not DATABASE_URL:
        # Default PostgreSQL connection
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "todoapp")
        
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # SQLite (default)
    DATABASE_URL = "sqlite:///./todos.db"

# Database pool settings
if USE_POSTGRESQL:
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "40"))
    DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    DB_POOL_PRE_PING = True
else:
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
    DB_POOL_RECYCLE = 3600
    DB_POOL_PRE_PING = False

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

if ENVIRONMENT == "production":
    allowed_origins = os.getenv("ALLOWED_ORIGINS")
    if allowed_origins:
        CORS_ORIGINS.extend(allowed_origins.split(","))

# Pagination
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 10
MAX_LIMIT = 100

# Search
MIN_SEARCH_LENGTH = 1
MAX_SEARCH_LENGTH = 100
MAX_SEARCH_RESULTS = 100

# Validation
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 500

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if DEBUG else "WARNING")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature flags
ENABLE_STATS = True
ENABLE_SEARCH = True
ENABLE_HEALTH_CHECK = True

# Timeouts
REQUEST_TIMEOUT = 30
DB_CONNECTION_TIMEOUT = 10

# Print config info on startup
def print_config():
    """Print configuration information"""
    print("=" * 60)
    print("Configuration Loaded")
    print("=" * 60)
    print(f"Environment: {ENVIRONMENT}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Database: {'PostgreSQL' if USE_POSTGRESQL else 'SQLite'}")
    print(f"Database URL: {DATABASE_URL}")
    print("=" * 60)
