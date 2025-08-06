import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# ─── API Configuration ──────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"

# ─── Available Models ───────────────────────────────────────────────────────
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile", 
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

OLLAMA_MODELS = [
    "llama3.2:3b",
    "nomic-embed-text:latest",
    "qwen3:4b",
    "granite3.2-vision:latest",
    "gemma2"
]

# ─── MySQL ──────────────────────────────────────────────────────────────────
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")

# ─── Databases to expose in UI ─────────────────────────────────────────────
DATABASES = os.getenv("ALLOWED_DATABASES", "").split(",")
