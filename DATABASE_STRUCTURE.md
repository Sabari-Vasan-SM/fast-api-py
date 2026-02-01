# Database Folder Structure

This document explains the new database folder structure and how it's organized.

## Folder Layout

```
server/
├── database/                      # Main database configuration folder
│   ├── __init__.py               # Package initialization
│   ├── config.py                 # PostgreSQL connection configuration
│   ├── init_db.py                # Database initialization script
│   └── migrations/               # Database migration files
│       ├── __init__.py
│       └── 001_initial_schema.sql # Initial database schema
│
├── app/
│   ├── database/                 # Legacy (deprecated)
│   │   └── db.py                # Now imports from database.config
│   ├── models/
│   │   ├── todo.py
│   │   └── schemas.py
│   └── routes/
│       └── todos.py
│
└── main.py
```

## Files Description

### database/config.py
**Purpose:** Main database configuration file
- Sets up PostgreSQL connection
- Defines database engine and session factory
- Handles environment variables for credentials
- Provides `get_db()` dependency for FastAPI routes

**Key Functions:**
- `get_db()` - FastAPI dependency for database sessions
- `get_engine()` - Returns the database engine instance

### database/init_db.py
**Purpose:** Database initialization and management
- Creates all tables from SQLAlchemy models
- Provides database reset capability (dangerous!)
- Verifies tables creation

**Usage:**
```bash
# Create tables
python database/init_db.py

# Reset database (delete all data)
python database/init_db.py reset
```

### database/migrations/001_initial_schema.sql
**Purpose:** SQL migration for initial schema setup
- Creates the `todos` table with all columns
- Creates indexes for optimized queries
- Can be run manually if needed

**Tables Created:**
- `todos` - Main table storing todo items
  - `id` - Primary key
  - `title` - Todo title (required)
  - `description` - Todo description (optional)
  - `completed` - Boolean status (default: false)
  - `created_at` - Timestamp (auto-generated)
  - `updated_at` - Timestamp (auto-updated)

**Indexes:**
- `idx_todos_completed` - For filtering by completion status
- `idx_todos_created_at` - For sorting by creation date

## How It Works

### 1. Connection Flow
```
main.py
  ↓
imports from database.config
  ↓
connects to PostgreSQL using DATABASE_URL from .env
  ↓
SessionLocal creates database sessions
```

### 2. Initialization Flow
```
python database/init_db.py
  ↓
Reads from app/models/todo.py (SQLAlchemy models)
  ↓
Creates tables in PostgreSQL database
  ↓
Verifies creation with information_schema query
```

### 3. API Request Flow
```
FastAPI Route (app/routes/todos.py)
  ↓
Calls get_db() dependency
  ↓
Returns database session from SessionLocal
  ↓
Session connects to PostgreSQL via engine
  ↓
Query executed, results returned
  ↓
Session closes in finally block
```

## Environment Variables

The database configuration requires these environment variables in `.env`:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=todoapp
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DEBUG=False
```

## Using with Docker Compose

The `docker-compose.yml` file in the root directory:
- Starts PostgreSQL 15 container
- Automatically runs migration files from `database/migrations/`
- Starts pgAdmin for database management
- Creates volumes for persistent data storage

## Migration Strategy

For future schema changes:

1. **Create new migration file:**
   ```
   database/migrations/002_add_column_priority.sql
   ```

2. **Add SQL changes:**
   ```sql
   ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 0;
   CREATE INDEX idx_todos_priority ON todos(priority);
   ```

3. **Run migration manually or with Docker Compose restart**

4. **Update SQLAlchemy models in `app/models/todo.py`**

## Best Practices

✓ Always use the `database.config` module for connections
✓ Use `get_db()` dependency in FastAPI routes
✓ Keep migration files version-numbered and dated
✓ Update `.env.example` when adding new variables
✓ Test migrations on a copy of production data first
✓ Use indexes for frequently queried columns
✓ Document schema changes in migration files

## Troubleshooting

**"No module named 'database'"**
- Make sure you're running scripts from the `server` directory
- Check that `.env` file exists with correct DATABASE_URL

**"FATAL: password authentication failed"**
- Verify DATABASE_USER and DATABASE_PASSWORD in .env
- Check PostgreSQL is running and accessible

**"database todoapp does not exist"**
- Run: `python database/init_db.py` to create tables
- Or manually: `createdb -U postgres todoapp`

**"relation \"todos\" does not exist"**
- Tables haven't been created yet
- Run: `python database/init_db.py`
