import brain_loader
import pywhatkit
import secrets
from elevenlabs.client import ElevenLabs
import pyaudio
import pyttsx3
import time
import pyautogui
import subprocess
import webbrowser
import cv2 
import skills 
import random
import requests 
import datetime 
import psutil    
import wikipedia 
import re 
import os  # ✅ FIXED: Added missing import

# --- CONFIG ---
try: 
    client = ElevenLabs(api_key=secrets.ELEVEN_KEY)
except: client = None

# ✅ VOICE: "Will" (Fast & Friendly)
VOICE_ID = "bIHbv24MWmeRgasZH58o" 
TTS_MODEL = "eleven_flash_v2_5" 

engine = pyttsx3.init()
try:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) 
except: pass
engine.setProperty('rate', 200)

# --- 🕉️ GITA API ---
def get_gita_specific(text):
    try:
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            ch = int(numbers[0]); sl = int(numbers[1])
        else:
            ch = random.randint(1, 18); sl = random.randint(1, 20)

        url = f"https://vedicscriptures.github.io/slok/{ch}/{sl}"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            sanskrit = data.get('slok', '').replace("\n", " ")
            hindi_meaning = data.get('tej', {}).get('ht', 'अर्थ उपलब्ध नहीं है।')
            return f"अध्याय {ch}, श्लोक {sl}: {sanskrit} ... अर्थ: {hindi_meaning}"
    except: pass
    return "Internet connection error, Sakha."

# --- 🕉️ MANTRA DATABASE ---
def get_mantra(text):
    if "gayatri" in text: return "ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्।"
    if "mrityunjaya" in text: return "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय मामृतात्॥"
    if "ganesh" in text: return "ॐ गं गणपतये नमो नमः। श्री सिद्धि विनायक नमो नमः।"
    if "shiv" in text: return "ॐ नमः शिवाय। हर हर महादेव।"
    if "hare" in text: return "हरे कृष्ण हरे कृष्ण, कृष्ण कृष्ण हरे हरे। हरे राम हरे राम, राम राम हरे हरे।"
    return "ॐ नमः शिवाय।"

# --- 🔋 SYSTEM INFO ---
def get_system_info(text):
    if "time" in text: return f"Samay hai {datetime.datetime.now().strftime('%I:%M %p')}."
    if "date" in text: return f"Aaj ki tareekh hai {datetime.datetime.now().strftime('%d %B %Y')}."
    if "battery" in text: 
        batt = psutil.sensors_battery()
        return f"Battery {batt.percent} pratishat hai."
    return None

# --- 🤔 THE MAIN BRAIN ---
def think(text):
    text = text.lower()

    # =================================================================
    # 🚨 PRIORITY 1: SYSTEM & OS COMMANDS (Strict Code)
    # =================================================================
    
    # Check Time/Date/Battery
    sys_info = get_system_info(text)
    if sys_info: return sys_info

    # App Control
    if "open" in text:
        app = text.replace("open", "").strip()
        skills.open_any_app(app)
        return f"Opening {app}."

    # Window Control
    if "close window" in text: pyautogui.hotkey('alt', 'f4'); return "Closed."
    if "minimize" in text: pyautogui.hotkey('win', 'd'); return "Done."
    
    # Shutdown
    if "shutdown" in text:
        os.system("shutdown /s /t 5")
        return "Shubh Ratri Sakha. System band kar raha hoon."

    # =================================================================
    # 🎵 PRIORITY 2: MEDIA (YouTube/Spotify)
    # =================================================================
    if "play" in text or "song" in text:
        song = text.replace("play", "").replace("song", "").strip()
        if "spotify" in text:
            skills.open_any_app("spotify"); time.sleep(3)
            pyautogui.hotkey('ctrl', 'l'); pyautogui.write(song); pyautogui.press('enter')
            return "Spotify par chala raha hoon."
        pywhatkit.playonyt(song)
        return f"Playing {song}."

    # =================================================================
    # 🕉️ PRIORITY 3: DIVINE KNOWLEDGE (Strict Hindi/Sanskrit)
    # =================================================================
    if "gita" in text or "geeta" in text or "chapter" in text:
        return get_gita_specific(text)

    if "chant" in text or "recite" in text or "mantra" in text or "bolo" in text:
        return get_mantra(text)

    # =================================================================
    # 🤖 PRIORITY 4: PHI-3 (ONLY FOR CASUAL TALK)
    # =================================================================
    # If the code reached here, it means NO command was found.
    # So, we let Phi-3 handle it as a conversation.
    
    print("💬 Neel Madhav (Phi-3) Chatting...")
    
    persona = (
        "You are Neel Madhav (Krishna). "
        "You are a friendly companion. "
        "You are NOT an assistant here, just a friend. "
        "Reply casually in Hinglish or Hindi. "
        "Keep it short."
    )
    
    return brain_loader.query(persona, text, mode="voice")

def speak_stream(text):
    if client:
        try:
            audio = client.text_to_speech.convert(
                text=text, 
                voice_id=VOICE_ID, 
                model_id=TTS_MODEL, 
                output_format="pcm_24000",
                optimize_streaming_latency=4 
            )
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
            for chunk in audio: stream.write(chunk)
            stream.stop_stream(); stream.close(); p.terminate()
            return 
        except: pass
    try: engine.say(text); engine.runAndWait()
    except: pass