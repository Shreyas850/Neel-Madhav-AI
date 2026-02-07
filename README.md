# 🦚 Neel Madhav AI (Krishna & Kanha)

> **A Divine Voice‑Activated Personal AI Assistant** blending modern artificial intelligence with spiritual wisdom.

**Neel Madhav** is a unique AI companion inspired by the persona of Lord Krishna. It serves two purposes:

1. A powerful **desktop AI assistant** for productivity and automation
2. A **spiritual guide** capable of reciting ancient scriptures with authentic pronunciation

Unlike typical cloud‑based assistants, Neel Madhav runs **locally on your GPU**, ensuring **maximum privacy**, **offline intelligence**, and **ultra‑fast responses**.

---

## 🌟 Key Capabilities

### 🧠 Dual AI Personalities

* **Krishna (The Wise)**
  Powered by **Phi‑3 Mini (4K context)** — ideal for deep philosophy, reasoning, and complex conversations.

* **Kanha (The Swift)**
  Powered by a **lightweight quantized model** — optimized for instant commands, witty replies, and rapid execution.

---

### ✨ Core Features

* **🕉️ Divine Wisdom**
  Recites *Bhagavad Gita* verses (Sanskrit & Hindi) and chants Vedic mantras with authentic pronunciation.

* **🗣️ Hyper‑Realistic Voice**
  Integrated with **ElevenLabs (Flash v2.5)** for human‑like speech with **<75 ms latency**.

* **💻 Desktop Automation**
  Control your PC hands‑free:

  * Shutdown / Restart system
  * Open or close applications
  * Minimize windows
  * Check battery, date, and time

* **🎵 Media Control**
  Voice‑controlled Spotify and YouTube playback.

* **🚀 Privacy‑First Architecture**
  Core intelligence runs **100% locally** using `llama-cpp-python` with **NVIDIA GPU acceleration**.

---

## 🛠️ Prerequisites

Ensure your system meets the following requirements:

* **OS:** Windows / Linux / macOS
  *(Windows recommended for full automation support)*
* **Python:** 3.10 or higher *(Tested on 3.12)*
* **Git:** Installed and available in PATH
* **Hardware:** NVIDIA GPU with CUDA Toolkit *(highly recommended)*

---

## 📥 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Shreyas850/Neel-Madhav-AI.git
cd Neel-Madhav-AI
```

---

### 2️⃣ Set Up Virtual Environment

#### 🪟 Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### 🐧 macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

#### Standard Install

```bash
pip install -r requirements.txt
```

#### ⚡ NVIDIA GPU Acceleration (Recommended)

Enable CUDA support for `llama-cpp-python`:

```bash
set CMAKE_ARGS=-DLLAMA_CUBLAS=on
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

---

## 🧠 Model Setup (The Brains)

Download the models and place them in the **root directory** of the project.

| Model Name      | Identity | Description                | Size    |
| --------------- | -------- | -------------------------- | ------- |
| **Phi‑3 Mini**  | Krishna  | Deep reasoning, philosophy | ~2.4 GB |
| **Jarvis Lite** | Kanha    | Fast commands, low memory  | ~1.1 GB |

### 📌 Rename the model files

```text
Phi‑3 Mini  →  krishna.gguf
Jarvis Lite →  kanha.gguf
```

---

## 🔑 Configuration & API Setup

### 1️⃣ Create Secrets File

* Locate `secrets_template.py`
* Rename it to `secrets.py`

### 2️⃣ Update API Keys

```python
# secrets.py

# ElevenLabs API (Required for Voice)
# Get your key from: https://elevenlabs.io/
ELEVEN_KEY = "your_elevenlabs_api_key"

# Database Configuration (Local setup)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "your_sql_password"
DB_NAME = "kanha_brain"
```

---

## 🚀 Usage

### ▶️ Start the Assistant

```bash
python launcher.py
```

---

### 🎙️ Voice Command Examples

| Category  | Command                | Action                 |
| --------- | ---------------------- | ---------------------- |
| Spiritual | "Recite Bhagavad Gita" | Recites a random verse |
| Verse     | "Chapter 2 Verse 47"   | Recites specific verse |
| Mantra    | "Chant Gayatri Mantra" | Vedic chanting         |
| Media     | "Play Hare Krishna"    | Plays on YouTube       |
| Apps      | "Open Spotify"         | Launches Spotify       |
| System    | "Shutdown System"      | Shuts down PC          |

---

## 🔄 Switching AI Brains

Edit `brain_loader.py`:

```python
# Options: "Krishna" or "Kanha"
ACTIVE_MODEL_NAME = "Kanha"
```

Restart the assistant to apply changes.

---

## 🙏 Credits & Acknowledgements

* **Phi‑3 Mini** by Microsoft
* **ElevenLabs** for ultra‑realistic Text‑to‑Speech
* **Vedic Scriptures API** for Bhagavad Gita verses
* Inspired by the eternal wisdom of **Sanatana Dharma**

---

<div align="center">

### 🦚 Jai Shree Krishna 🦚

**Built with ❤️ by Shreyas850**

</div>
