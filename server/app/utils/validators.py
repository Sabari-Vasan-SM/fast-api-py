"""
Validation utilities for the Todo application
"""
from typing import Optional


def validate_todo_title(title: str) -> bool:
    """Validate todo title"""
    if not title or not isinstance(title, str):
        return False
    title = title.strip()
    if len(title) < 1 or len(title) > 255:
        return False
    return True


def validate_todo_description(description: Optional[str]) -> bool:
    """Validate todo description"""
    if description is None:
        return True
    if not isinstance(description, str):
        return False
    if len(description) > 500:
        return False
    return True


def sanitize_title(title: str) -> str:
    """Sanitize and clean up todo title"""
    return title.strip()


def sanitize_description(description: Optional[str]) -> Optional[str]:
    """Sanitize and clean up todo description"""
    if description is None:
        return None
    return description.strip()


def normalize_query(query: str) -> str:
    """Normalize search query"""
    return query.strip().lower()
