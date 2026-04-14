import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# This is your "Advice" map - simple for now.
EXPERT_MAP = {
    "creative": "meta-llama/llama-3-70b-instruct",
    "fast": "openai/gpt-4o-mini",
    "logic": "anthropic/claude-3.5-sonnet"
}

@app.route('/v1/chat/completions', methods=['POST'])
def proxy_request():
    # 1. Get the user's intent
    data = request.json
    category = data.get("category", "fast")
    model = EXPERT_MAP.get(category)
    
    # 2. Call OpenRouter (The starting point)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
        json={
            "model": model,
            "messages": data.get("messages")
        }
    )
    
    # 3. Basic Logging for your 2%
    # In Phase 2, this goes to a database. For now, we print it.
    usage = response.json().get("usage", {})
    print(f"DEBUG: Used {model}. Usage: {usage}")
    
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000)