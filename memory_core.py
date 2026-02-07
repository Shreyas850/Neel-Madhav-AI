import json
import os

MEMORY_FILE = "brain_data.json"

# Default Brain Structure
DEFAULT_DATA = {
    "user_name": "Sir",
    "assistant_name": "Diya",
    "history": [] # Stores last 10 conversations
}

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except: return DEFAULT_DATA

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_history(user_text, ai_text):
    data = load_memory()
    # Keep strictly the last 6 exchanges to prevent lag
    history = data.get("history", [])
    history.append(f"User: {user_text}")
    history.append(f"Diya: {ai_text}")
    if len(history) > 6: history = history[-6:]
    
    data["history"] = history
    save_memory(data)

def get_context():
    data = load_memory()
    name = data.get("user_name", "Sir")
    recent_chat = "\n".join(data.get("history", []))
    return f"User Name: {name}\nRecent Conversation:\n{recent_chat}"

def set_name(name):
    data = load_memory()
    data["user_name"] = name
    save_memory(data)