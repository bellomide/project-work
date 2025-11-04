# Medical Chatbot Backend (FastAPI)

This is a **FastAPI-based backend** for a medical chatbot that provides basic health information and symptom guidance. It leverages **NLP (Natural Language Processing)** to understand user queries and respond intelligently.

---

## Features
- Built with **FastAPI** for high performance and async processing.
- Handles medical-related text queries using **spaCy** and **NLTK**.
- Simple REST API endpoints for chatbot communication.
- Modular design with `main.py` (API routes) and `model.py` (NLP logic).
- Easy deployment to services like Render or Heroku.

---

## Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Language:** Python 3.9+
- **NLP Tools:** spaCy, NLTK
- **Deployment:** Gunicorn + Uvicorn workers

---

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-chatbot-backend.git
   cd medical-chatbot-backend
