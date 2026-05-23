# 🤖 Bonny — AI Health-Support-Through-Chat-Bot
(Educational Demo)

> **⚠️ DISCLAIMER:** This project is strictly for **educational and demonstration purposes only**.
> It is **NOT** a replacement for real mental health services or professional crisis intervention.
> If you or someone you know is in crisis, please contact a professional immediately.

---

## 📌 Overview

**Bonny** is an AI-powered conversational chatbot designed to demonstrate how natural language processing can be used to detect mental health risk signals in real time. It uses a locally running **Ollama LLM (llama3.2)** for generating empathetic responses and applies a **keyword-based semantic risk checker** to classify messages into three categories:

| Risk Level | Trigger | Response |
|---|---|---|
| 🚨 **Danger** | Suicidal language detected | Emergency message + SMS alert (optional) |
| 😔 **Depression** | Depressive language detected | PHQ-9 inspired empathetic questions |
| ✅ **Normal** | General conversation | Standard LLM response via Ollama |

---

## 🗂️ Project Structure

```
sprint/
├── app.py                  # Main Flask application & routing
├── config.py               # Configuration (Ollama URL, thresholds, SMS settings)
├── semantic_check.py       # Keyword-based risk classification
├── sms_alert.py            # Optional Twilio SMS alert on danger detection
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Landing page
│   ├── warning.html        # Educational disclaimer page
│   └── chat.html           # Main chatbot UI
└── README.md               # This file
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| LLM | [Ollama](https://ollama.com/) with `llama3.2` model |
| Risk Detection | Custom keyword similarity (`semantic_check.py`) |
| SMS Alerts | Twilio (optional, disabled by default) |
| Frontend | Vanilla HTML, CSS, JavaScript |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/download) installed and running locally
- `llama3.2` model pulled in Ollama

### 1. Pull the Ollama Model

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting the app:

```bash
ollama serve
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python app.py
```

The app will start at: **http://127.0.0.1:5000**

---

## 🌐 Application Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing / welcome page |
| `/warning` | GET | Educational disclaimer page |
| `/chat` | GET | Chatbot UI |
| `/chat` | POST | Send a message and receive a response |

---

## 🧠 How It Works

### Risk Detection Flow

```
User Message
     │
     ▼
semantic_check.py
     │
     ├─── Danger keywords detected? ──► Emergency message + SMS alert
     │
     ├─── Depression keywords detected? ──► PHQ-9 style empathy prompt → Ollama
     │
     └─── Normal ──► Forward to Ollama → Return response
```

### Danger Keywords (examples)
- `suicide`, `end my life`, `kill myself`, `want to die`

### Depression Keywords (examples)
- `feeling down`, `lost interest`, `depressed`, `hopeless`

---

## 🔧 Configuration (`config.py`)

All settings can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_URL` | `http://127.0.0.1:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2` | Model name to use |
| `DANGER_SIM_THRESHOLD` | `0.55` | Threshold score to flag as danger |
| `DEPRESSION_SIM_THRESHOLD` | `0.45` | Threshold score to flag as depression |
| `EMERGENCY_SMS_ENABLED` | `false` | Enable Twilio SMS alerts |
| `TWILIO_ACCOUNT_SID` | *(empty)* | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | *(empty)* | Twilio Auth Token |
| `TWILIO_FROM` | *(empty)* | Twilio sender phone number |
| `OWNER_PHONE` | *(empty)* | Phone number to receive alerts |

---

## 📱 Optional: SMS Alerts (Twilio)

To enable SMS alerts when a danger message is detected:

1. Sign up at [twilio.com](https://www.twilio.com/)
2. Set the following environment variables (or edit `config.py`):

```bash
set EMERGENCY_SMS_ENABLED=true
set TWILIO_ACCOUNT_SID=your_account_sid
set TWILIO_AUTH_TOKEN=your_auth_token
set TWILIO_FROM=+1xxxxxxxxxx
set OWNER_PHONE=+91xxxxxxxxxx
```

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|---|---|---|
| `Ollama error: 500` | Model still loading into memory | Wait a few seconds and retry |
| `Cannot connect to Ollama` | Ollama not running | Run `ollama serve` in terminal |
| `ModuleNotFoundError: flask` | Virtual env not activated | Run `.\venv\Scripts\activate` |
| `Timeout` error | llama3.2 is slow on first request | App now waits up to 120 seconds |

---

## 🆘 Real Crisis Resources (India)

If you or someone you know is in crisis, please reach out immediately:

- **Emergency Services:** 108 or 102
- **iCall (Crisis Helpline):** 9152987821
- **KIRAN Mental Health Helpline:** 1800-599-0019 (Free, 24/7)
- **Aasra (Suicide Prevention):** +91-11-23389090

---

## 📄 License

This project is for **educational purposes only**. Use responsibly.

---

*Built with ❤️ using Flask + Ollama (llama3.2)*
