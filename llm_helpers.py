import requests
import json
from config import GROQ_API_KEY, GROQ_ENDPOINT, OLLAMA_ENDPOINT

def nl_to_sql_groq(nl_query: str, db_name: str, schema: dict, model: str) -> str:
    """Turn NL request into pure SQL via Groq."""
    schema_json = json.dumps(schema, indent=2)
    system_prompt = f"""
You are an expert MySQL assistant.
The database `{db_name}` has this schema:
{schema_json}

Rules:
• Generate ONLY safe SELECT statements.
• Use ONLY the tables/columns shown above.
• Add LIMIT 100 to big-result queries unless user says otherwise.
• Return ONLY the raw SQL (no markdown, no explanation).
• Use INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, CROSS JOIN, SELF JOIN according to the nl query don't use only JOIN.
"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Database: {db_name}\nQuery: {nl_query}"}
        ],
        "max_tokens": 512,
        "temperature": 0.1
    }
    
    res = requests.post(
        GROQ_ENDPOINT,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    if not res.ok:
        raise Exception(f"GROQ API {res.status_code}: {res.text}")

    content = res.json()["choices"][0]["message"]["content"]
    lines = [ln for ln in content.splitlines()
             if ln.strip() and not ln.lower().startswith(("sql", "```"))
            ]
    return " ".join(lines).replace("`", "").strip()

def nl_to_sql_ollama(nl_query: str, db_name: str, schema: dict, model: str) -> str:
    """Turn NL request into pure SQL via Ollama."""
    schema_json = json.dumps(schema, indent=2)
    system_prompt = f"""
You are an expert MySQL assistant.
The database `{db_name}` has this schema:
{schema_json}

Rules:
-  Generate ONLY safe SELECT statements.
-  Use ONLY the tables/columns shown above.
-  Add LIMIT 100 to big-result queries unless user says otherwise.
-  Return ONLY the raw SQL (no markdown, no explanation).
-  Use INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, CROSS JOIN, SELF JOIN according to the nl query don't use only JOIN.
"""
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Database: {db_name}\nQuery: {nl_query}"}
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 512
        }
    }
    
    try:
        res = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=30)
        if not res.ok:
            raise Exception(f"Ollama API {res.status_code}: {res.text}")
        
        content = res.json()["message"]["content"]
        lines = [ln for ln in content.splitlines()
                 if ln.strip() and not ln.lower().startswith(("sql", "```"))]
        return " ".join(lines).replace("`", "").strip()
        
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
    except requests.exceptions.Timeout:
        raise Exception("Ollama request timed out. The model might be loading.")

def nl_to_sql(nl_query: str, db_name: str, schema: dict, provider: str, model: str) -> str:
    """Main function to route to appropriate LLM provider."""
    if provider == "Groq":
        return nl_to_sql_groq(nl_query, db_name, schema, model)
    elif provider == "Ollama":
        return nl_to_sql_ollama(nl_query, db_name, schema, model)
    else:
        raise Exception(f"Unknown provider: {provider}")
