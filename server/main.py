"""
Todo API - FastAPI Application
A RESTful API for managing todos with SQLite/PostgreSQL
"""
import logging
import os
from datetime import datetime
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.config import engine
from app.models.todo import Base
from app.routes import todos
from app.routes import auth as auth_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
USE_POSTGRESQL = os.getenv("USE_POSTGRESQL", "false").lower() == "true"

# Initialize database tables
def init_database():
    """Initialize database tables on startup"""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database initialized successfully")
        logger.info(f"Using database: {'PostgreSQL' if USE_POSTGRESQL else 'SQLite'}")
    except Exception as e:
        logger.error(f"✗ Error initializing database: {e}")
        raise

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="A modern REST API for managing todos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
cors_origins = [
    "http://localhost:5173",      # Vite dev server
    "http://localhost:3000",      # Alternative frontend
    "http://localhost:8080",      # Alternative frontend
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

if ENVIRONMENT == "production":
    cors_origins.append("https://yourdomain.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)


# ============================================================================
# EVENT HANDLERS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("=" * 60)
    logger.info("🚀 Todo API Starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug Mode: {DEBUG}")
    logger.info("=" * 60)
    init_database()


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("=" * 60)
    logger.info("🛑 Todo API Shutting Down...")
    logger.info("=" * 60)


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/", response_model=Dict)
def read_root():
    """
    Root endpoint - Welcome message
    """
    return {
        "message": "Welcome to Todo API",
        "version": "1.0.0",
        "documentation": "/docs",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/info", response_model=Dict)
def get_info():
    """Get API information and status"""
    return {
        "name": "Todo API",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "database": "PostgreSQL" if USE_POSTGRESQL else "SQLite",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", response_model=Dict)
def health_check():
    """
    Health check endpoint
    Returns application and database status
    """
    try:
        from database.config import SessionLocal
        db = SessionLocal()
        
        # Test database connection
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "service": "todo-api",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "1.0.0"
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "todo-api",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


# ============================================================================
# ROUTE INCLUSION
# ============================================================================


# Include todos and auth routers
app.include_router(todos.router)
app.include_router(auth_routes.router)

logger.info("Routes registered successfully")


# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
        log_level="info"
    )
