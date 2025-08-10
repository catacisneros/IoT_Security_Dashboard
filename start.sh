#!/bin/bash

echo "🚀 Starting IoT Security Dashboard..."

# Start backend in background
echo "📡 Starting FastAPI backend..."
cd "$(dirname "$0")"
python Main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🖥️  Starting React frontend..."
cd iot-dashboard
npm start &
FRONTEND_PID=$!

echo "✅ Both services started!"
echo "📡 Backend: http://localhost:8000"
echo "🖥️  Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
