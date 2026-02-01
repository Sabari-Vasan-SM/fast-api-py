# This module is deprecated. Use database.config instead.
# Kept for backward compatibility.

from database.config import engine, SessionLocal, get_db

__all__ = ['engine', 'SessionLocal', 'get_db']
