#!/bin/bash
# Launch script for the Streamlit AgGrid Demo

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is available
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit not found. Please install dependencies first:"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Launch the app
echo "🚀 Starting Streamlit AgGrid Demo..."
echo "📊 The app will open automatically in your browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
