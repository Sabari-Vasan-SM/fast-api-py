# Architecture & Data Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT TIER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Svelte + Vite Application                  │  │
│  │  (Port: 5173)                                            │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ Components:                                     │   │  │
│  │  │ - App.svelte                                   │   │  │
│  │  │ - AddTodo.svelte                               │   │  │
│  │  │ - TodoItem.svelte                              │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ Stores (State Management):                      │   │  │
│  │  │ - todos.js (Svelte store with Axios)           │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                     HTTP/REST API Calls
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     SERVER TIER                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         FastAPI Application (Port: 8000)                │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Routes (API Endpoints):                         │   │  │
│  │  │ - GET /api/todos                                │   │  │
│  │  │ - POST /api/todos                               │   │  │
│  │  │ - PUT /api/todos/{id}                           │   │  │
│  │  │ - DELETE /api/todos/{id}                        │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Models & Schemas:                               │   │  │
│  │  │ - SQLAlchemy ORM (todo.py)                       │   │  │
│  │  │ - Pydantic Schemas (schemas.py)                 │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      Database Configuration & Session Management       │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ database/config.py:                            │   │  │
│  │  │ - Engine creation                               │   │  │
│  │  │ - Session factory                               │   │  │
│  │  │ - Connection pooling                            │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ database/init_db.py:                            │   │  │
│  │  │ - Table creation                                │   │  │
│  │  │ - Database initialization                       │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                         SQL Queries
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA TIER                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      PostgreSQL Database (Port: 5432)                   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Schema:                                         │   │  │
│  │  │ ┌─ todos table ─────────────────────────────┐  │   │  │
│  │  │ │ id          SERIAL PRIMARY KEY            │  │   │  │
│  │  │ │ title       VARCHAR(255) NOT NULL        │  │   │  │
│  │  │ │ description VARCHAR(500)                 │  │   │  │
│  │  │ │ completed   BOOLEAN DEFAULT FALSE        │  │   │  │
│  │  │ │ created_at  TIMESTAMP DEFAULT NOW()      │  │   │  │
│  │  │ │ updated_at  TIMESTAMP DEFAULT NOW()      │  │   │  │
│  │  │ └─────────────────────────────────────────┘  │   │  │
│  │  │ Indexes:                                      │   │  │
│  │  │ - idx_todos_completed                        │   │  │
│  │  │ - idx_todos_created_at                       │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ pgAdmin (Optional Web UI)                      │   │  │
│  │  │ Port: 5050                                     │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↑
                        Docker Network
                              ↑
                    docker-compose.yml
```

## Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. USER INTERACTION IN FRONTEND                               │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ User clicks "Add Todo" button in AddTodo.svelte     │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  2. FORM SUBMISSION                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ handleSubmit() called with title and description   │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  3. API CALL VIA STORE                                         │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ todos.js: addTodo() calls:                           │   │
│     │ POST /api/todos with JSON data                      │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  4. FASTAPI ROUTING                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ app/routes/todos.py:                                │   │
│     │ @router.post("/") receives request                 │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  5. DATA VALIDATION                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ Pydantic TodoCreate schema validates input         │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  6. DATABASE SESSION                                           │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ get_db() dependency injects database session       │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  7. ORM OPERATION                                              │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ SQLAlchemy Todo model creates instance             │   │
│     │ db.add(db_todo)                                    │   │
│     │ db.commit()                                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  8. DATABASE QUERY                                             │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ PostgreSQL receives INSERT statement:               │   │
│     │ INSERT INTO todos (title, description, ...)        │   │
│     │ VALUES (...)                                       │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  9. DATA PERSISTED                                             │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ New todo record stored in PostgreSQL               │   │
│     │ Auto-generated ID returned                         │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│ 10. RESPONSE RETURNED                                          │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ FastAPI returns TodoResponse with:                  │   │
│     │ - id                                                │   │
│     │ - title                                             │   │
│     │ - created_at                                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│ 11. FRONTEND UPDATE                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ Svelte store updated: todos.update()               │   │
│     │ Component reactively re-renders                    │   │
│     │ New todo appears in list                           │   │
│     └──────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│ 12. USER SEES RESULT                                           │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ New todo visible in Todo List                       │   │
│     │ Form cleared for next input                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Folder Structure Hierarchy

```
fast-api-py/
│
├─ Client Layer (Svelte)
│  ├─ UI Components
│  │  ├─ AddTodo
│  │  ├─ TodoItem
│  │  └─ App (Main)
│  ├─ State (Store)
│  │  └─ todos (with Axios API calls)
│  └─ Build Config
│     ├─ Vite
│     └─ Svelte
│
├─ Server Layer (FastAPI)
│  ├─ API Routes
│  │  └─ todos (CRUD endpoints)
│  ├─ Business Logic
│  │  ├─ Models (SQLAlchemy ORM)
│  │  └─ Schemas (Pydantic validation)
│  └─ Infrastructure
│     ├─ Database Config
│     ├─ Session Management
│     └─ Migrations
│
└─ Data Layer (PostgreSQL)
   ├─ Todos Table
   ├─ Indexes
   └─ Constraints
```

## Technology Stack Layers

```
┌────────────────────────────────────────────────────────────────┐
│                      PRESENTATION                              │
│              Svelte Components + HTML/CSS                      │
│                    (Port: 5173)                                │
└────────────────────────────────────────────────────────────────┘
                              ↑
                            Axios
                          (JSON/HTTP)
                              ↓
┌────────────────────────────────────────────────────────────────┐
│                    APPLICATION                                 │
│            FastAPI + Uvicorn ASGI Server                       │
│                    (Port: 8000)                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Routes → Pydantic → Business Logic → Session Management │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              ↑
                         SQLAlchemy ORM
                           (SQL/psycopg2)
                              ↓
┌────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS                                 │
│           SQLAlchemy Engine + Connection Pool                  │
└────────────────────────────────────────────────────────────────┘
                              ↑
                       PostgreSQL Protocol
                              ↓
┌────────────────────────────────────────────────────────────────┐
│                    DATABASE                                    │
│           PostgreSQL 15 (Docker Container)                     │
│                    (Port: 5432)                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Query Execution → Indexes → Tables → Data Storage       │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## Development & Deployment

```
                    DEVELOPMENT
                        ↓
    ┌─────────────────────────────────────┐
    │  Docker Compose (Local)             │
    │  - PostgreSQL 15                    │
    │  - pgAdmin                          │
    │  - Auto-initialization              │
    └─────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────┐
    │  FastAPI Dev Server                 │
    │  - Auto-reload                      │
    │  - Debug logs                       │
    └─────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────┐
    │  Svelte Dev Server                  │
    │  - Hot module reload                │
    │  - API proxy                        │
    └─────────────────────────────────────┘
                        ↓
                   TESTING
                        ↓
                  PRODUCTION
                        ↓
    ┌─────────────────────────────────────┐
    │  FastAPI + Gunicorn                 │
    │  - Multiple workers                 │
    │  - Connection pooling               │
    └─────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────┐
    │  PostgreSQL Instance                │
    │  - Backups & replication            │
    │  - Performance monitoring           │
    └─────────────────────────────────────┘
```
