"""
Database initialization script
Run this to create all tables in the database
"""

import sys
import os

# Add server directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database.config import engine, SessionLocal
from app.models.todo import Base


def init_db():
    """Initialize database with all tables"""
    try:
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")

        # Check if tables exist
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            )
            tables = result.fetchall()
            print(f"\n✓ Created tables: {[table[0] for table in tables]}")

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped!")
    except Exception as e:
        print(f"✗ Error dropping tables: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        print("WARNING: This will delete all data!")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            drop_all_tables()
            init_db()
        else:
            print("Cancelled.")
    else:
        init_db()
