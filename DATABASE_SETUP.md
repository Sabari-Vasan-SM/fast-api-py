# PostgreSQL Database Setup Guide

## Prerequisites
- Docker and Docker Compose installed
- OR PostgreSQL 14+ installed locally

## Option 1: Using Docker Compose (Recommended)

### Start PostgreSQL
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL on port 5432
- Create the `todoapp` database
- Start pgAdmin on port 5050 (optional, for database management)

### Stop PostgreSQL
```bash
docker-compose down
```

### View PostgreSQL logs
```bash
docker-compose logs postgres
```

## Option 2: Local PostgreSQL Installation

### Windows
1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. PostgreSQL will run as a service by default

### macOS
```bash
brew install postgresql@15
brew services start postgresql@15
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

## Database Configuration

### Update .env file
Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/todoapp
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=todoapp
DATABASE_USER=postgres
DATABASE_PASSWORD=password
```

## Initialize Database

### Create database tables:
```bash
# From server directory with virtual environment activated
python database/init_db.py
```

### Reset database (delete all data):
```bash
python database/init_db.py reset
```

## Verify Connection

### Using psql (command line):
```bash
psql -U postgres -h localhost -d todoapp
```

### Connect and check tables:
```sql
\dt  -- List all tables
SELECT * FROM todos;  -- View todos table
\q   -- Quit
```

### Using pgAdmin (Web UI):
1. Open http://localhost:5050
2. Login with: admin@example.com / admin
3. Add Server:
   - Host: postgres (or localhost if local)
   - Port: 5432
   - Username: postgres
   - Password: password

## Troubleshooting

### "Could not connect to database"
- Check if PostgreSQL is running: `sudo service postgresql status`
- Verify credentials in .env file
- Ensure port 5432 is not blocked by firewall

### "Database does not exist"
- Create database: `createdb -U postgres todoapp`
- Or run: `python database/init_db.py`

### "psycopg2 import error"
- Reinstall dependencies: `pip install -r requirements.txt`

## Useful PostgreSQL Commands

```bash
# List all databases
psql -U postgres -l

# Create database
createdb -U postgres todoapp

# Drop database
dropdb -U postgres todoapp

# Backup database
pg_dump -U postgres todoapp > backup.sql

# Restore database
psql -U postgres todoapp < backup.sql
```

## Next Steps

1. Start the FastAPI server: `python main.py`
2. Access API docs: http://localhost:8000/docs
3. Start the Svelte client: `npm run dev` (from client folder)
4. Access app: http://localhost:5173
