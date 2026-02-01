# PostgreSQL Useful Commands & Queries

## Command Line (psql)

### Connection
```bash
# Connect to database
psql -U postgres -h localhost -d todoapp

# Connect with password prompt
psql -U postgres -h localhost -d todoapp -W
```

### Database Management
```bash
# List all databases
\l

# Switch to different database
\c todoapp

# List all tables
\dt

# List table structure
\d todos

# List indexes
\di

# Exit psql
\q
```

## Useful SQL Queries

### View All Todos
```sql
SELECT * FROM todos;
```

### Count Todos
```sql
-- Total todos
SELECT COUNT(*) FROM todos;

-- Completed todos
SELECT COUNT(*) FROM todos WHERE completed = true;

-- Pending todos
SELECT COUNT(*) FROM todos WHERE completed = false;
```

### Find Todos by Status
```sql
-- Get all completed todos
SELECT * FROM todos WHERE completed = true;

-- Get all pending todos
SELECT * FROM todos WHERE completed = false;
```

### Search Todos
```sql
-- Search by title (case insensitive)
SELECT * FROM todos WHERE LOWER(title) LIKE LOWER('%search term%');

-- Search by description
SELECT * FROM todos WHERE description LIKE '%search term%';
```

### Sort & Filter
```sql
-- Recent todos first
SELECT * FROM todos ORDER BY created_at DESC;

-- Oldest todos first
SELECT * FROM todos ORDER BY created_at ASC;

-- Completed first, then pending
SELECT * FROM todos ORDER BY completed DESC, created_at DESC;

-- Get with limit
SELECT * FROM todos LIMIT 10 OFFSET 0;
```

### Statistics
```sql
-- Completion rate
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN completed = true THEN 1 END) as completed,
  ROUND(100.0 * COUNT(CASE WHEN completed = true THEN 1 END) / COUNT(*), 2) as completion_rate
FROM todos;

-- Todos by creation date
SELECT DATE(created_at), COUNT(*) 
FROM todos 
GROUP BY DATE(created_at)
ORDER BY DATE(created_at) DESC;

-- Average time to complete (if last_completed tracked)
SELECT 
  title,
  created_at,
  updated_at,
  EXTRACT(DAY FROM (updated_at - created_at)) as days_to_complete
FROM todos
WHERE completed = true;
```

## Data Modification

### Insert Data
```sql
INSERT INTO todos (title, description, completed) 
VALUES ('Buy groceries', 'Milk, eggs, bread', false);

-- Multiple inserts
INSERT INTO todos (title, description, completed) VALUES 
('Task 1', 'Description 1', false),
('Task 2', 'Description 2', false),
('Task 3', 'Description 3', true);
```

### Update Data
```sql
-- Mark as complete
UPDATE todos SET completed = true WHERE id = 1;

-- Update multiple fields
UPDATE todos 
SET title = 'New Title', description = 'New Description'
WHERE id = 1;

-- Toggle completion
UPDATE todos 
SET completed = NOT completed 
WHERE id = 1;

-- Update all pending
UPDATE todos 
SET completed = true 
WHERE completed = false AND created_at < NOW() - INTERVAL '7 days';
```

### Delete Data
```sql
-- Delete specific todo
DELETE FROM todos WHERE id = 1;

-- Delete completed todos
DELETE FROM todos WHERE completed = true;

-- Delete all todos
DELETE FROM todos;
-- Reset sequence
ALTER SEQUENCE todos_id_seq RESTART WITH 1;
```

## Database Maintenance

### Backup Database
```bash
# Backup to file
pg_dump -U postgres -h localhost todoapp > backup.sql

# Backup with compression
pg_dump -U postgres -h localhost todoapp | gzip > backup.sql.gz
```

### Restore Database
```bash
# Restore from backup
psql -U postgres -h localhost todoapp < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | psql -U postgres -h localhost todoapp
```

### Analyze & Optimize
```sql
-- Analyze table for query planning
ANALYZE todos;

-- Vacuum to free space
VACUUM todos;

-- Full vacuum (locks table)
VACUUM FULL todos;
```

### Check Database Size
```sql
-- Database size
SELECT pg_size_pretty(pg_database_size('todoapp'));

-- Table size
SELECT pg_size_pretty(pg_total_relation_size('todos'));

-- Index size
SELECT pg_size_pretty(pg_relation_size('idx_todos_completed'));
```

## Performance Tips

### Create Index for Better Performance
```sql
-- Index on frequently searched columns
CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_created_at ON todos(created_at DESC);

-- Composite index for common queries
CREATE INDEX idx_todos_status_date ON todos(completed, created_at DESC);
```

### Check Query Performance
```sql
-- Explain query plan (shows how query will be executed)
EXPLAIN SELECT * FROM todos WHERE completed = false;

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM todos WHERE completed = false;
```

## User Management

### Create New User
```sql
CREATE USER todoapp_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE todoapp TO todoapp_user;
GRANT USAGE ON SCHEMA public TO todoapp_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO todoapp_user;
```

### Change Password
```sql
ALTER USER todoapp_user WITH PASSWORD 'new_password';
```

### Drop User
```sql
DROP USER todoapp_user;
```

## Common Issues & Solutions

### Table Already Exists
```sql
-- Drop existing table
DROP TABLE IF EXISTS todos CASCADE;
```

### Primary Key Conflicts
```sql
-- Reset sequence
ALTER SEQUENCE todos_id_seq RESTART WITH 1;
```

### Locks on Table
```sql
-- View active connections
SELECT * FROM pg_stat_activity;

-- Terminate connection
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'postgres';
```

## Using with Python/SQLAlchemy

### Raw SQL in FastAPI
```python
from sqlalchemy import text
from database.config import SessionLocal

def get_raw_todos():
    db = SessionLocal()
    result = db.execute(text("SELECT * FROM todos WHERE completed = :status"), {"status": False})
    todos = result.fetchall()
    db.close()
    return todos
```

### Using ORM
```python
from app.models.todo import Todo
from database.config import SessionLocal

def get_pending_todos():
    db = SessionLocal()
    todos = db.query(Todo).filter(Todo.completed == False).all()
    db.close()
    return todos
```
