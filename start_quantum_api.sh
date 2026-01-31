#!/bin/bash

echo "🌈 LUXBIN Light Language - Quantum Communication API"
echo "=================================================="
echo ""
echo "🔬 Optimized for Diamond NV Center Quantum Computers"
echo "📡 Universal Communication Protocol"
echo ""

# Check if FastAPI is installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing FastAPI dependencies..."
    pip3 install fastapi uvicorn pydantic
fi

echo "🚀 Starting Quantum API Server..."
echo ""
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔄 Interactive API: http://localhost:8000/redoc"
echo "🔑 Demo API Key: demo_key_for_testing"
echo ""
echo "📚 See API_GUIDE.md for complete documentation"
echo ""

# Start the server
python3 light_language_api.py
