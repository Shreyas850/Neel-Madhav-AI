import speech_recognition as sr
import whisper
import torch
import numpy as np
import os

# --- CONFIGURATION ---
MODEL_SIZE = "base"
ENERGY_THRESHOLD = 500  # Adjusted for sensitivity
PAUSE_THRESHOLD = 0.6   # Adjusted for speed

print(f"\n🎧 Loading Whisper Model ({MODEL_SIZE}) to GPU...")

try:
    # Force usage of NVIDIA GPU (cuda)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Load model to GPU
    audio_model = whisper.load_model(MODEL_SIZE, device=device)
    print(f"✅ Whisper Ears Active on {device.upper()}.")
except Exception as e:
    print(f"❌ Error loading Whisper: {e}")
    device = "cpu"
    audio_model = whisper.load_model(MODEL_SIZE, device="cpu")

def listen_loop(callback_function):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.pause_threshold = PAUSE_THRESHOLD
    recognizer.dynamic_energy_threshold = True 

    microphone = sr.Microphone()

    print("🎤 Adjusting for ambient noise... (Please stay quiet)")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Ready to Listen.")

    while True:
        try:
            with microphone as source:
                print("👂 Listening...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                
                print("🧠 Transcribing...")
                
                # --- 🚀 RAM-ONLY PROCESSING (No Files) ---
                # 1. Get raw PCM audio data resampled to 16000Hz (Whisper's native rate)
                raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
                
                # 2. Convert raw bytes to Float32 NumPy array
                # (Divide by 32768.0 to normalize between -1.0 and 1.0)
                audio_np = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0

                # 3. Transcribe directly from RAM
                result = audio_model.transcribe(
                    audio_np, 
                    fp16=torch.cuda.is_available(),
                    language='en' # Optional: Remove if you want auto-detection
                )
                
                text = result['text'].strip()

                if text:
                    print(f"🗣️ User said: {text}")
                    callback_function(text)
                else:
                    # Silence the "Ghost" logs to keep console clean
                    # print("Example: (Silence)") 
                    pass

        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"❌ Hearing Error: {e}")