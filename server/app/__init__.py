"""
FastAPI application package
Main application entry point and configuration
"""

__version__ = "1.0.0"
__author__ = "Todo API"
__description__ = "A modern REST API for managing todos"

from app.models.todo import Base, Todo
from app.models.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.routes import todos

__all__ = [
    'Base',
    'Todo',
    'TodoCreate',
    'TodoUpdate',
    'TodoResponse',
    'todos',
]
