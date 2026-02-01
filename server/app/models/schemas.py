"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """Base todo schema with common fields"""
    title: str = Field(..., min_length=1, max_length=255, description="Todo title")
    description: Optional[str] = Field(None, max_length=500, description="Todo description")
    completed: bool = Field(False, description="Completion status")

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not empty after stripping"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('description')
    def description_strip(cls, v):
        """Strip whitespace from description"""
        if v:
            return v.strip()
        return v


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not empty after stripping"""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        if v:
            return v.strip()
        return v

    @validator('description')
    def description_strip(cls, v):
        """Strip whitespace from description"""
        if v:
            return v.strip()
        return v


class TodoResponse(TodoBase):
    """Schema for todo response with metadata"""
    id: int = Field(..., description="Todo ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2024-02-01T10:30:00",
                "updated_at": "2024-02-01T10:30:00"
            }
        }


class TodoStats(BaseModel):
    """Schema for todo statistics"""
    total: int = Field(..., description="Total todos")
    completed: int = Field(..., description="Completed todos")
    pending: int = Field(..., description="Pending todos")
    completion_rate: float = Field(..., description="Completion percentage")


class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    database: str = Field(..., description="Database connection status")
