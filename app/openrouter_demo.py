import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_model(
    prompt: str, 
    model: str = "openai/gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 1000
):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(BASE_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(ask_model("Hello! Can you give me a motivational quote?"))
