#!/bin/bash

echo "🚀 Setting up AI-Data Platform Demo..."

# Create data directory if not exists
mkdir -p backend/data

# Backend Setup
echo "📦 Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend Setup
echo "🎨 Setting up Frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup Complete!"
echo ""
echo "To run the demo:"
echo "1. Terminal 1 (Backend): cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "2. Terminal 2 (Frontend): cd frontend && npm run dev"
