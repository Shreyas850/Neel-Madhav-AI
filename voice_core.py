import speech_recognition as sr

def listen_loop(callback):
    r = sr.Recognizer()
    r.energy_threshold = 280
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        print("🎤 Calibrating... (Silence please)")
        r.adjust_for_ambient_noise(source, duration=1)
        print("✅ LISTENING ACTIVE.")
        
        while True:
            try:
                # Listen
                audio = r.listen(source, timeout=None, phrase_time_limit=10)
                
                try:
                    # 'en-IN' ensures it understands Indian accents better
                    text = r.recognize_google(audio, language="en-IN")
                    if text:
                        callback(text)
                except sr.UnknownValueError:
                    pass 
            except sr.RequestError:
                print("⚠️ Internet Error")
            except Exception as e:
                print(f"Mic Error: {e}")