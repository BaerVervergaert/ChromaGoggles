#!/bin/bash
# Quick start script for ChromaGoggles

echo "🎨 ChromaGoggles - Starting application..."
echo ""
echo "This will launch the Streamlit web interface."
echo "Press Ctrl+C to stop the application."
echo ""

# Check if streamlit is available
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    poetry install
fi

# Run the application
echo "🚀 Launching ChromaGoggles..."
poetry run streamlit run main.py

