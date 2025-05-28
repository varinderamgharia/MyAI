from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 1: Put your API key here directly
OPENROUTER_API_KEY = "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"

@app.post("/")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    messages = [
        {
            "role": "system",
            "content": (
                "Tusi ek chatbot ho jo sirf Punjabi vich gal kar da, "
                "par angrezi alphabet naal. English translation na karo."
            )
        },
        {"role": "user", "content": user_input}
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": messages,
        "temperature": 0.8
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers
    )

    try:
        result = response.json()
        if "choices" not in result:
            return {"error": "OpenRouter returned no choices", "full_response": result}
        return {"reply": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": "API error", "details": str(e)}
