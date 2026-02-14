"""
SQLAlchemy models for todo application
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index, Text
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Todo(Base):
    """Todo model for database storage"""
    __tablename__ = "todos"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core fields
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="todos")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_todos_completed', 'completed'),
        Index('idx_todos_created_at', 'created_at'),
        Index('idx_todos_title', 'title'),
        Index('idx_todos_completed_created', 'completed', 'created_at'),
    )

    def __repr__(self):
        """String representation of todo"""
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"

    def to_dict(self):
        """Convert todo to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    class Config:
        from_attributes = True
