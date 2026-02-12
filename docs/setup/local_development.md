# Local Development Setup Guide

## Prerequisites

- Node.js 16+ and npm
- Python 3.9+
- PostgreSQL 12+
- Git

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` and configure:
```
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=Project Sachet
VITE_APP_VERSION=0.1.0
```

### 3. Run Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Build for Production
```bash
npm run build
npm run preview
```

## Backend Setup

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` and configure:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/sachet_db
JWT_SECRET_KEY=your-jwt-secret-key
```

### 4. Database Setup
```bash
# Initialize database
flask db upgrade

# Or manually create:
createdb sachet_db
flask shell
# In Flask shell:
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 5. Run Development Server
```bash
flask run
```

The backend API will be available at `http://localhost:5000`

## Running Both Servers

Use two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
flask run
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Database

### PostgreSQL Setup (macOS/Linux)
```bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb sachet_db

# Access PostgreSQL
psql -U postgres -d sachet_db
```

### PostgreSQL Setup (Windows)
1. Download and install PostgreSQL from postgres.org
2. Use pgAdmin to create a new database named `sachet_db`
3. Update `DATABASE_URL` in backend `.env`

## Troubleshooting

### Port Already in Use
- Frontend default: 5173
- Backend default: 5000

Change in `frontend/vite.config.ts` or `backend/run.py`

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env`
- Check database credentials

### Module Not Found Errors
- Reinstall dependencies: `npm install` or `pip install -r requirements.txt`
- Clear cache and rebuild

## Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
python -m pytest
```

---

For more information, see the main [README.md](../README.md)
