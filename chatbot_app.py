from flask import Flask, render_template, request, jsonify
import cohere
from duckduckgo_search import DDGS
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

# API KEY
co = cohere.Client("ENTER API")

print("AI Chatbot Started...")

# Memory
chat_history = []

# Internet Search
def internet_search(query):

    results = DDGS().text(query, max_results=3)

    search_text = ""

    for r in results:

        search_text += f"Title: {r['title']}\n"
        search_text += f"Content: {r['body']}\n\n"

    return search_text

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Chat Route
@app.route("/chat", methods=["POST"])
def chat():

    user = request.json["message"]

    # Save user message
    chat_history.append({
        "role": "USER",
        "message": user
    })

    # Internet Search
    search_results = internet_search(user)

    # Prompt with internet data
    prompt = f"""
Use this internet information if useful:

{search_results}

User Question:
{user}
"""

    # AI Response
    response = co.chat(
        message=prompt,
        chat_history=chat_history
    )

    ai_reply = response.text

    # Save AI reply
    chat_history.append({
        "role": "CHATBOT",
        "message": ai_reply
    })

    # Keep last 10 messages
    if len(chat_history) > 10:
        del chat_history[:-10]

    return jsonify({
        "reply": ai_reply
    })

# Run Server
if __name__ == "__main__":
    app.run(debug=True)