# 🦚 Neel Madhav AI (Krishna & Kanha)

> **A Divine Voice-Activated Personal AI Assistant** blending modern artificial intelligence with spiritual wisdom.

**Neel Madhav** is a unique AI companion inspired by the persona of Lord Krishna. It serves two purposes:

1. A powerful **desktop AI assistant** for productivity and automation  
2. A **spiritual guide** capable of reciting ancient scriptures with authentic pronunciation  

Unlike typical cloud-based assistants, Neel Madhav runs **locally on your GPU**, ensuring **maximum privacy**, **offline intelligence**, and **ultra-fast responses**.

---

# 🌟 Key Capabilities

## 🧠 Dual AI Personalities

### Krishna (The Wise)
Powered by **Phi-3 Mini (4K context)** — ideal for deep philosophy, reasoning, and complex conversations.

### Kanha (The Swift)
Powered by a **lightweight quantized model** — optimized for instant commands, witty replies, and rapid execution.

---

# ✨ Core Features

### 🕉️ Divine Wisdom
Recites **Bhagavad Gita** verses (Sanskrit & Hindi) and chants Vedic mantras with authentic pronunciation.

### 🗣️ Hyper-Realistic Voice
Integrated with **ElevenLabs (Flash v2.5)** for human-like speech with **<75 ms latency**.

### 💻 Desktop Automation
Control your PC hands-free:

- Shutdown / Restart system  
- Open or close applications  
- Minimize windows  
- Check battery, date, and time  

### 🎵 Media Control
Voice-controlled **Spotify** and **YouTube** playback.

### 🚀 Privacy-First Architecture
Core intelligence runs **100% locally** using `llama-cpp-python` with **NVIDIA GPU acceleration**.

---

# 🛠️ Prerequisites

Ensure your system meets the following requirements:

- **OS:** Windows / Linux / macOS  
  *(Windows recommended for full automation support)*  
- **Python:** 3.10 or higher *(Tested on 3.12)*  
- **Git:** Installed and available in PATH  
- **Hardware:** NVIDIA GPU with CUDA Toolkit *(highly recommended)*  

---

# 📥 Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Shreyas850/Neel-Madhav-AI.git
cd Neel-Madhav-AI
```

---

## 2️⃣ Set Up Virtual Environment

### 🪟 Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 🐧 macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

### Standard Install

```bash
pip install -r requirements.txt
```

### ⚡ NVIDIA GPU Acceleration (Recommended)

Enable CUDA support for **llama-cpp-python**:

```bash
set CMAKE_ARGS=-DLLAMA_CUBLAS=on
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

---

# 🧠 Model Setup (The Brains)

Download the models and place them in the **root directory of the project**.

🔗 **Official model download page (both models)**  
[https://huggingface.co/Khush2007/Neel-MadhavPhi3/tree/main](https://huggingface.co/Khush2007/Neel-Madhav-Phi3)

| Model Name | Identity | Description | Size |
|------------|----------|-------------|------|
| **Phi-3 Mini** | Krishna | Deep reasoning, philosophy | ~2.4 GB |
| **Jarvis Lite** | Kanha | Fast commands, low memory | ~1.1 GB |

### 📌 Rename the model files

```
Phi-3 Mini  →  krishna.gguf
Jarvis Lite →  kanha.gguf
```

---

# 💻 Laptop / CPU-Only Mode

If you are running **Neel Madhav AI on a laptop or CPU-only system (no NVIDIA GPU)**, use the following settings to prevent crashes and reduce RAM usage.

---

## 1️⃣ Update `brain_loader.py` (The Brain)

Change the Llama initialization to lower memory usage and force CPU processing:

```python
# Laptop Friendly Configuration
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,          # Lower context to save RAM (Standard is 4096)
    n_gpu_layers=0,      # 0 = Force CPU (Prevents GPU VRAM errors)
    verbose=False
)
```

---

## 2️⃣ Update `voice_core.py` (The Ears)

Force Whisper to use the CPU and automatically fall back to a smaller model if required:

```python
# Force CPU for Whisper Ears
try:
    # 'base' model is a good balance for modern CPUs
    audio_model = whisper.load_model("base", device="cpu")
    print("✅ Whisper Ears Active on CPU.")
except:
    # 'tiny' model is faster for older laptops
    audio_model = whisper.load_model("tiny", device="cpu")
    print("⚠️ Fallback to Tiny model on CPU.")
```

---

# 🔑 Configuration & API Setup

## 1️⃣ Create Secrets File

Create a new file named:

```
app_secrets.py
```

in the **root directory**.

⚠️ **Do NOT name it `secrets.py`** because it can conflict with Python’s internal modules.

---

## 2️⃣ Update API Keys

Copy this template into `app_secrets.py`:

```python
# app_secrets.py

# --- 🗄️ DATABASE CREDENTIALS ---
# (Required for Neel Madhav's Long-Term Memory)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "your_sql_password_here"
DB_NAME = "kanha_brain"


# --- 🔑 AI API KEYS ---

# Hugging Face Token (Optional, for downloading models)
HF_TOKEN = "your_hf_token_here"

# Gemini API (For general intelligence & chat)
GEMINI_KEY = "your_gemini_key_here"

# ElevenLabs API (For Realistic Voice - Krishna/Radha)
# Get your key from: https://elevenlabs.io/
ELEVEN_KEY = "your_elevenlabs_key_here"


# --- 🌐 EXTERNAL SERVICES ---

# News API (For fetching latest headlines)
NEWS_API_KEY = "your_news_api_key_here"

# Weather API (For live weather updates)
WEATHER_API_KEY = "your_weather_api_key_here"
```

⚠️ **Security Tip**

Add this to your `.gitignore` file:

```
app_secrets.py
```

This prevents accidentally uploading your **private API keys to GitHub**.

---

# 🚀 Usage

## ▶️ Start the Assistant

```bash
python launcher.py
```

---

# 🎙️ Voice Command Examples

| Category | Command | Action |
|--------|--------|--------|
| Spiritual | "Recite Bhagavad Gita" | Recites a random verse |
| Verse | "Chapter 2 Verse 47" | Recites specific verse |
| Mantra | "Chant Gayatri Mantra" | Vedic chanting |
| Media | "Play Hare Krishna" | Plays on YouTube |
| Apps | "Open Spotify" | Launches Spotify |
| System | "Shutdown System" | Shuts down PC |

---

# 🔄 Switching AI Brains

Edit **brain_loader.py**

```python
# Options: "Krishna" or "Kanha"
ACTIVE_MODEL_NAME = "Kanha"
```

Restart the assistant to apply changes.

---

# 🙏 Credits & Acknowledgements

- **Phi-3 Mini** by Microsoft  
- **ElevenLabs** for ultra-realistic Text-to-Speech  
- **Vedic Scriptures API** for Bhagavad Gita verses  
- Inspired by the eternal wisdom of **Sanatana Dharma**

---

<div align="center">

### 🦚 Jai Shree Krishna 🦚  
**Built with ❤️ by Shreyas850**

</div>
