"""
Open WebUI Configuration for local deployment
"""
import os

# API Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Server Configuration
PORT = 3001
HOST = "0.0.0.0"

# Available Models
AVAILABLE_MODELS = [
    {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI"},
    {"id": "openai/gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
    {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku", "provider": "Anthropic"},
    {"id": "anthropic/claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
    {"id": "mistralai/mistral-7b-instruct", "name": "Mistral 7B", "provider": "Mistral"},
    {"id": "google/gemini-pro", "name": "Gemini Pro", "provider": "Google"},
]

# Default Settings
DEFAULT_MODEL = "openai/gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
DEFAULT_SYSTEM_PROMPT = ""

print("📋 Open WebUI Configuration:")
print(f"🔑 OpenRouter API Key: {'✅ Set' if OPENROUTER_API_KEY else '❌ Not set'}")
print(f"🔑 OpenAI API Key: {'✅ Set' if OPENAI_API_KEY else '❌ Not set'}")
print(f"🌐 Server will run on: http://{HOST}:{PORT}")
print(f"🤖 Default Model: {DEFAULT_MODEL}")
print(f"📊 Available Models: {len(AVAILABLE_MODELS)} models configured")
