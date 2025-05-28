from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Allow cross-origin calls (so your frontend can talk to it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read your OpenRouter key from an environment variable
OPENROUTER_API_KEY = os.getenv("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")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    # Tell the model: “Reply only in Punjabi (English letters)”
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
        "Authorization": f"Bearer {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}"
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
        return {"reply": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": "API error", "details": str(e)}
