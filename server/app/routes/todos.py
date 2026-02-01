"""
Todo API routes with CRUD operations and advanced features
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.models.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.database.db import get_db
from app.utils.validators import (
    validate_todo_title,
    validate_todo_description,
    sanitize_title,
    sanitize_description,
    normalize_query,
)
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/todos", tags=["todos"])


# ============================================================================
# GET ENDPOINTS
# ============================================================================

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    skip: int = Query(0, ge=0, description="Number of todos to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum todos to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort: str = Query("date", regex="^(date|title)$", description="Sort by date or title"),
    db: Session = Depends(get_db)
):
    """
    Get all todos with pagination, filtering, and sorting.
    
    - **skip**: Offset for pagination (default: 0)
    - **limit**: Max results (default: 10, max: 100)
    - **completed**: Filter by true/false (optional)
    - **sort**: Sort by 'date' (default) or 'title'
    """
    try:
        query = db.query(Todo)
        
        # Apply status filter
        if completed is not None:
            query = query.filter(Todo.completed == completed)
        
        # Apply sorting
        if sort == "title":
            query = query.order_by(Todo.title.asc())
        else:  # default: date
            query = query.order_by(desc(Todo.created_at))
        
        # Apply pagination
        todos = query.offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(todos)} todos (skip={skip}, limit={limit})")
        return todos
    
    except Exception as e:
        logger.error(f"Error fetching todos: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch todos")


@router.get("/stats", response_model=Dict)
def get_todo_stats(db: Session = Depends(get_db)):
    """Get statistics about todos"""
    try:
        total = db.query(Todo).count()
        completed = db.query(Todo).filter(Todo.completed == True).count()
        pending = total - completed
        
        stats = {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        }
        
        logger.info(f"Todo stats: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch stats")


@router.get("/search/{query}", response_model=List[TodoResponse])
def search_todos(
    query: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search todos by title or description.
    
    - **query**: Search term
    - **limit**: Max results (default: 10, max: 100)
    """
    if not query or len(query.strip()) < 1:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    try:
        search_term = normalize_query(query)
        todos = db.query(Todo).filter(
            or_(
                Todo.title.ilike(f"%{search_term}%"),
                Todo.description.ilike(f"%{search_term}%")
            )
        ).limit(limit).all()
        
        logger.info(f"Search results for '{query}': {len(todos)} todos found")
        return todos
    
    except Exception as e:
        logger.error(f"Error searching todos: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search todos")


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            logger.warning(f"Todo with ID {todo_id} not found")
            raise HTTPException(status_code=404, detail="Todo not found")
        
        logger.info(f"Retrieved todo with ID {todo_id}")
        return todo
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching todo {todo_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch todo")


# ============================================================================
# POST ENDPOINTS
# ============================================================================

@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo.
    
    - **title**: Todo title (required, 1-255 chars)
    - **description**: Optional description (max 500 chars)
    - **completed**: Completion status (default: false)
    """
    try:
        # Validate input
        if not validate_todo_title(todo.title):
            raise HTTPException(
                status_code=400,
                detail="Invalid title. Must be 1-255 characters"
            )
        
        if not validate_todo_description(todo.description):
            raise HTTPException(
                status_code=400,
                detail="Invalid description. Max 500 characters"
            )
        
        # Sanitize input
        title = sanitize_title(todo.title)
        description = sanitize_description(todo.description)
        
        # Create todo
        db_todo = Todo(
            title=title,
            description=description,
            completed=todo.completed or False
        )
        
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        
        logger.info(f"Created new todo with ID {db_todo.id}: {title}")
        return db_todo
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating todo: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create todo")


# ============================================================================
# PUT ENDPOINTS
# ============================================================================

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a todo. Only provided fields are updated.
    
    - **title**: Optional new title
    - **description**: Optional new description
    - **completed**: Optional completion status
    """
    try:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            logger.warning(f"Todo with ID {todo_id} not found for update")
            raise HTTPException(status_code=404, detail="Todo not found")
        
        update_data = todo_update.dict(exclude_unset=True)
        
        # Validate and sanitize updates
        if "title" in update_data:
            if not validate_todo_title(update_data["title"]):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid title. Must be 1-255 characters"
                )
            update_data["title"] = sanitize_title(update_data["title"])
        
        if "description" in update_data:
            if not validate_todo_description(update_data["description"]):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid description. Max 500 characters"
                )
            update_data["description"] = sanitize_description(update_data["description"])
        
        # Update timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        
        logger.info(f"Updated todo with ID {todo_id}")
        return db_todo
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update todo")


# ============================================================================
# DELETE ENDPOINTS
# ============================================================================

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a specific todo by ID"""
    try:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            logger.warning(f"Todo with ID {todo_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Todo not found")
        
        db.delete(db_todo)
        db.commit()
        
        logger.info(f"Deleted todo with ID {todo_id}")
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete todo")


@router.delete("/clear-completed", status_code=204)
def delete_all_completed(db: Session = Depends(get_db)):
    """Delete all completed todos"""
    try:
        deleted_count = db.query(Todo).filter(Todo.completed == True).delete()
        db.commit()
        
        logger.info(f"Deleted {deleted_count} completed todos")
        return None
    
    except Exception as e:
        logger.error(f"Error clearing completed todos: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear completed todos")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health", response_model=Dict)
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.query(Todo).first()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service unavailable - database connection failed"
        )
