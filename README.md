# 📝 Todo List Application

A simple, fast, and modern Todo List app built with **FastAPI** (backend) and **Svelte** (frontend).

## 🚀 Quick Start

### Backend Setup

```bash
cd server

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install & run
pip install -r requirements.txt
python -m database.init_db
python main.py
```

**API:** http://localhost:8000  
**Docs:** http://localhost:8000/docs

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

**App:** http://localhost:5173

---

## 📊 Features

✅ Create, update, delete todos  
✅ Mark complete/incomplete  
✅ Search & filter todos  
✅ Sort by date or status  
✅ Descriptions & timestamps  
✅ Auto API documentation  
✅ Error handling & validation  
✅ Pagination support  

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all todos |
| GET | `/api/todos/{id}` | Get single todo |
| POST | `/api/todos` | Create todo |
| PUT | `/api/todos/{id}` | Update todo |
| DELETE | `/api/todos/{id}` | Delete todo |
| GET | `/api/todos/search/{query}` | Search |
| DELETE | `/api/todos/clear-completed` | Clear completed |

### Query Parameters

```
GET /api/todos?skip=0&limit=10&status=active&sort=date
```

---

## 🛠️ Tech Stack

- **FastAPI** - Python web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Svelte 4** - UI framework
- **Vite** - Build tool
- **SQLite/PostgreSQL** - Database

---

## 📦 Project Structure

```
├── server/
│   ├── app/
│   │   ├── models/      (database & schemas)
│   │   ├── routes/      (API endpoints)
│   │   └── utils/       (helpers)
│   ├── database/        (DB config & init)
│   ├── main.py
│   └── requirements.txt
├── client/
│   ├── src/
│   │   ├── components/
│   │   └── stores/
│   └── package.json
└── README.md
```

---

## 🗄️ Database

**SQLite** (default - no setup needed)

**PostgreSQL** (optional):
```env
USE_POSTGRESQL=true
DATABASE_URL=postgresql://postgres:password@localhost:5432/todoapp
```

---

## 💡 Example Usage

```bash
# Create
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2% milk"}'

# Get all
curl http://localhost:8000/api/todos?limit=5

# Search
curl http://localhost:8000/api/todos/search/milk

# Update
curl -X PUT http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete
curl -X DELETE http://localhost:8000/api/todos/1
```

---

## 📄 License

MIT
