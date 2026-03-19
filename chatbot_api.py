from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import re

app = FastAPI()

# Allow website to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load intents
with open("ai/intents.json") as file:
    data = json.load(file)


# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


# Chatbot logic
def get_response(message):

    message = clean_text(message)

    best_match = None
    best_score = 0

    for intent in data["intents"]:
        for pattern in intent["patterns"]:

            pattern = clean_text(pattern)

            # Word matching score
            pattern_words = pattern.split()
            msg_words = message.split()

            score = sum(1 for word in pattern_words if word in msg_words)

            if score > best_score:
                best_score = score
                best_match = intent

    # If good match found
    if best_match and best_score > 0:
        return random.choice(best_match["responses"])

    return "I'm not sure about that. Please contact our enterprise security team."


# API endpoint
@app.post("/chat")
async def chat(request: dict):

    message = request.get("message", "")

    if not message:
        return {"reply": "Please enter a message."}

    reply = get_response(message)

    return {"reply": reply}