import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine database type from environment or use SQLite by default
use_postgresql = os.getenv("USE_POSTGRESQL", "false").lower() == "true"

if use_postgresql:
    # PostgreSQL configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('DATABASE_USER', 'postgres')}:{os.getenv('DATABASE_PASSWORD', 'password')}@{os.getenv('DATABASE_HOST', 'localhost')}:{os.getenv('DATABASE_PORT', '5432')}/{os.getenv('DATABASE_NAME', 'todoapp')}"
    )
    pool_config = {"poolclass": StaticPool}
else:
    # SQLite configuration (default)
    DATABASE_URL = "sqlite:///./todos.db"
    pool_config = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}

print(f"Using database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False") == "True",
    **pool_config
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    """Get the database engine"""
    return engine
