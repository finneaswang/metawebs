#!/bin/bash

echo "🚀 Starting Open WebUI Deployment"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "deploy_openwebui.py" ]; then
    echo "❌ Please run this script from the Metaweb directory"
    exit 1
fi

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📋 Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
fi

# Check for API keys
if [ -z "$OPENROUTER_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: No API keys found!"
    echo "Please set your API key:"
    echo "  export OPENROUTER_API_KEY='your_key_here'"
    echo "  OR"
    echo "  export OPENAI_API_KEY='your_key_here'"
    echo ""
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment"
    source venv/bin/activate
fi

# Run the deployment script
echo "🚀 Running deployment script..."
python3 deploy_openwebui.py
