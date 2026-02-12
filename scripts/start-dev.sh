#!/bin/bash

# Project Sachet - Start Development Servers

echo "🚀 Starting Project Sachet development servers..."

# Start backend in background
echo "▶️  Starting backend server..."
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
flask run --host=127.0.0.1 --port=5000 &
BACKEND_PID=$!
echo "   Backend running on http://localhost:5000 (PID: $BACKEND_PID)"

# Start frontend
echo "▶️  Starting frontend server..."
cd ../frontend
echo "   Frontend running on http://localhost:5173"
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
