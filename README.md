# Todo List Application - FastAPI + Svelte

A simple, modern Todo List application built with FastAPI backend and Svelte frontend.

## Project Structure

```
fast-api-py/
├── client/                 # Svelte frontend
│   ├── src/
│   │   ├── components/    # Reusable Svelte components
│   │   │   ├── AddTodo.svelte
│   │   │   └── TodoItem.svelte
│   │   ├── stores/        # Svelte stores (state management)
│   │   │   └── todos.js
│   │   ├── App.svelte     # Main App component
│   │   └── main.js        # Entry point
│   ├── public/            # Static files
│   ├── index.html         # HTML template
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.js     # Vite configuration
│   └── svelte.config.js   # Svelte configuration
│
├── server/                # FastAPI backend
│   ├── app/
│   │   ├── models/        # Database models and schemas
│   │   │   ├── todo.py
│   │   │   └── schemas.py
│   │   ├── routes/        # API endpoints
│   │   │   └── todos.py
│   │   ├── database/      # Database configuration
│   │   │   └── db.py
│   │   └── __init__.py
│   ├── main.py           # FastAPI app entry point
│   └── requirements.txt   # Backend dependencies
│
└── README.md
```

## Features

- ✅ Create, Read, Update, Delete (CRUD) todos
- ✅ Mark todos as complete/incomplete
- ✅ Add descriptions to todos
- ✅ View creation date for each todo
- ✅ Filter todos by completion status
- ✅ Modern, responsive UI
- ✅ Real-time updates with Svelte stores
- ✅ CORS-enabled API

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## API Endpoints

- `GET /api/todos` - Get all todos
- `GET /api/todos/{id}` - Get a specific todo
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `GET /health` - Health check endpoint

## Building for Production

### Backend

The FastAPI app is production-ready. Use a production server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend

Build the Svelte app:

```bash
npm run build
```

This creates an optimized `dist` folder that can be served by any static file server.

## Technologies Used

- **Backend:**
  - FastAPI
  - SQLAlchemy
  - SQLite
  - Pydantic

- **Frontend:**
  - Svelte
  - Vite
  - Axios
  - CSS3

## License

MIT
