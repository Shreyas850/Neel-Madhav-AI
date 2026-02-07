import speech_recognition as sr
import whisper
import torch
import os
import threading

# --- CONFIGURATION ---
# Options: "tiny", "base", "small", "medium", "large"
# "base" is the sweet spot for speed vs accuracy on GPU.
MODEL_SIZE = "base"
ENERGY_THRESHOLD = 300  # Adjust for background noise (300-400 is good)
PAUSE_THRESHOLD = 0.8   # Time to wait before considering command "finished"

print(f"\n🎧 Loading Whisper Model ({MODEL_SIZE}) to GPU...")

try:
    # Force usage of NVIDIA GPU (cuda)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    audio_model = whisper.load_model(MODEL_SIZE, device=device)
    print(f"✅ Whisper Ears Active on {device.upper()}.")
except Exception as e:
    print(f"❌ Error loading Whisper: {e}")
    print("⚠️ Falling back to CPU (slower)...")
    audio_model = whisper.load_model(MODEL_SIZE, device="cpu")

def listen_loop(callback_function):
    """
    Continuous listening loop using SpeechRecognition for VAD 
    and OpenAI Whisper for transcription.
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.pause_threshold = PAUSE_THRESHOLD
    
    # Dynamic noise adjustment
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
                # Listen until silence is detected
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                
                print("🧠 Transcribing...")
                
                # 1. Save temporary wav file (Whisper likes files)
                with open("temp_command.wav", "wb") as f:
                    f.write(audio.get_wav_data())

                # 2. Transcribe using Local GPU Model
                # fp16=False fixes some CPU/older GPU errors
                result = audio_model.transcribe(
                    "temp_command.wav", 
                    fp16=torch.cuda.is_available(),
                    language='en' # You can remove this to auto-detect Hindi/English
                )
                
                text = result['text'].strip()

                # 3. Cleanup & Callback
                if text:
                    print(f"🗣️ User said: {text}")
                    callback_function(text)
                else:
                    print("Example: (Silence)")

        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"❌ Hearing Error: {e}")