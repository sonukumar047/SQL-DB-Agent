import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# ─── Groq API ───────────────────────────────────────────────────────────────
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL         = "llama-3.3-70b-versatile"

# ─── MySQL ──────────────────────────────────────────────────────────────────
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")

# ─── Databases to expose in UI ─────────────────────────────────────────────
DATABASES = os.getenv("ALLOWED_DATABASES", "").split(",")
