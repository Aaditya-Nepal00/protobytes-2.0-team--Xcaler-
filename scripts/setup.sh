#!/bin/bash

# Project Sachet - Initial Setup Script

echo "🚀 Setting up Project Sachet..."

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed."; exit 1; }
command -v python >/dev/null 2>&1 || { echo "Python is required but not installed."; exit 1; }
command -v psql >/dev/null 2>&1 || { echo "PostgreSQL is required but not installed."; exit 1; }

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
cp .env.example .env
npm install
cd ..

# Backend setup
echo "📦 Setting up backend..."
cd backend
cp .env.example .env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo "✅ Setup complete!"
echo "📖 Next steps:"
echo "1. Configure environment variables in .env files"
echo "2. Setup database: createdb sachet_db"
echo "3. Run migrations: cd backend && flask db upgrade"
echo "4. Start servers: run start-dev.sh"
