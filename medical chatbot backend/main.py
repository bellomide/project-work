# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import MedicalAdviceModel  # Changed from relative import
import os 


# Create FastAPI app
app = FastAPI(
    title="Simple Medical Chatbot API",
    description="A lightweight AI chatbot backend for basic medical advice and symptom checking.",
    version="1.0.0"
)

# CORS Configuration - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify: ["http://localhost:3000", "https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your model
model = MedicalAdviceModel()

# Define request body format
class ChatRequest(BaseModel):
    user_input: str


# ============= MAIN CHAT ENDPOINT =============
@app.post("/chat")
def get_medical_advice(request: ChatRequest):
    """
    Endpoint to get medical advice based on user input.
    Returns a formatted text response for the chatbot.
    """
    user_message = request.user_input
    result = model.predict(user_message)
    
    # Format response for frontend
    if result.get("success"):
        # Build a conversational response
        response_text = f"**{result['condition']}**\n\n"
        
        response_text += "**Symptoms:**\n"
        for symptom in result['symptoms'][:5]:  # Show top 5 symptoms
            response_text += f"• {symptom}\n"
        
        response_text += "\n**Medical Advice:**\n"
        for i, advice in enumerate(result['advice'][:4], 1):  # Show top 4 advice
            response_text += f"{i}. {advice}\n"
        
        response_text += "\n**Prevention Tips:**\n"
        for tip in result['prevention'][:3]:  # Show top 3 prevention tips
            response_text += f"• {tip}\n"
        
        response_text += f"\n⚠️ {result['disclaimer']}"
        
        return {"response": response_text}
    else:
        # Handle no match found
        available = ", ".join([c.replace("_", " ").title() for c in result.get("available_conditions", [])])
        return {
            "response": f"{result['message']}\n\nI can help with: {available}"
        }


# ============= CONDITIONS LIST ENDPOINT =============
@app.get("/conditions")
def list_conditions():
    """
    Returns a list of all conditions known by the chatbot.
    Format: {"conditions": ["Malaria", "Typhoid", ...]}
    """
    conditions = model.get_all_conditions()
    # Convert underscores to spaces and title case
    formatted_conditions = [c.replace("_", " ").title() for c in conditions]
    
    return {"conditions": formatted_conditions}


# ============= CONDITION DETAILS ENDPOINT =============
@app.get("/condition/{condition_name}")
def get_condition_info(condition_name: str):
    """
    Returns detailed information (symptoms, advice, prevention) about a given condition.
    """
    result = model.get_condition_info(condition_name)
    
    if result.get("success"):
        # Return formatted response
        return {
            "condition": result["condition"],
            "symptoms": result["symptoms"],
            "advice": "\n".join([f"{i}. {a}" for i, a in enumerate(result["advice"], 1)]),
            "prevention": result["prevention"],
            "disclaimer": result["disclaimer"]
        }
    else:
        # Return error with available conditions
        available = [c.replace("_", " ").title() for c in result.get("available_conditions", [])]
        return {
            "error": result["error"],
            "available_conditions": available
        }


# ============= ROOT ENDPOINT =============
@app.get("/")
def root():
    """
    Welcome message to test if API is running.
    """
    return {
        "message": "Welcome to the Simple Medical Chatbot API 💊",
        "status": "running",
        "endpoints": {
            "POST /chat": "Send symptoms or condition to get advice",
            "GET /conditions": "List all known conditions",
            "GET /condition/{condition_name}": "Get detailed info for one condition"
        }
    }


# ============= HEALTH CHECK =============
@app.get("/health")
def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy", "model_loaded": model is not None}


# Optional: Serve static frontend if you have one
# Uncomment these lines if you have a template folder with frontend.html
# app.mount("/static", StaticFiles(directory="template"), name="static")
# 
# @app.get("/frontend", response_class=HTMLResponse)
# def get_frontend():
#     frontend_path = os.path.join("template", "frontend.html")
#     with open(frontend_path, "r", encoding="utf-8") as f:
#         return f.read()