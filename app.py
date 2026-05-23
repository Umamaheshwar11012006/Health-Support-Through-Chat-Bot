from flask import Flask, request, render_template, jsonify
import requests
import time
import config
from semantic_check import check_message
from sms_alert import send_alert

app = Flask(__name__)

# Store flagged users in memory (replace with DB later)
flagged_users = {}

def forward_to_ollama(msg: str):
    res = None
    try:
        res = requests.post(
            config.OLLAMA_URL,
            json={"model": config.OLLAMA_MODEL, "prompt": msg, "stream": False},
            timeout=120  # increased from 30s — llama3.2 can be slow on first load
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except requests.exceptions.HTTPError as e:
        error_details = res.text if res is not None else str(e)
        return f"⚠️ Ollama returned an error. Please try again in a few seconds. (Details: {error_details})"
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to Ollama. Please make sure Ollama is running on your laptop."
    except requests.exceptions.Timeout:
        return "⚠️ Ollama is taking too long to respond. The model may still be loading — please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"

# ---------- ROUTES ----------
@app.route("/")
def index():
    # Main landing page
    return render_template("index.html")

@app.route("/warning")
def warning_page():
    # Educational purpose warning page
    return render_template("warning.html")

@app.route("/chat")
def chat_page():
    # The actual chatbot interface page
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    user = request.form.get("user", "anon")
    msg = request.form.get("msg", "")

    # Semantic risk check
    risk, score = check_message(msg)

    if risk == "danger":
        flagged_users[user] = {"msg": msg, "risk": "danger", "time": time.ctime()}
        send_alert(msg)
        return jsonify(reply="🚨 I'm worried about your safety. Please call a helpline or emergency services right now.")

    elif risk == "depression":
        flagged_users[user] = {"msg": msg, "risk": "depression", "time": time.ctime()}
        hidden_prompt = (
            "Ask the user subtle mood-check questions inspired by the PHQ-9 depression scale. "
            "Do not say it's a test. Be conversational and empathetic."
        )
        reply = forward_to_ollama(hidden_prompt + "\nUser: " + msg)
        return jsonify(reply=reply)

    else:
        reply = forward_to_ollama(msg)
        return jsonify(reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
