import time
import psutil
import threading
import datetime
import pyttsx3 # We use a lightweight local TTS for alerts (faster than ElevenLabs)

# --- CONFIG ---
CHECK_INTERVAL = 60  # Check every 60 seconds

class AutonomyCore:
    def __init__(self, voice_engine):
        self.engine = voice_engine
        self.stop_flag = False
        self.last_battery = 100
        self.greeted_morning = False
        
    def start(self):
        thread = threading.Thread(target=self.loop)
        thread.daemon = True
        thread.start()

    def speak_alert(self, text):
        """Standard alerts use the main voice engine"""
        print(f"\n[⚠️ SYSTEM ALERT] {text}")
        self.engine(text)

    def loop(self):
        print("⚡ Autonomy Systems Online: Monitoring Hardware...")
        while not self.stop_flag:
            try:
                # 1. BATTERY MONITOR
                battery = psutil.sensors_battery()
                if battery:
                    plugged = battery.power_plugged
                    percent = battery.percent
                    
                    if not plugged and percent < 20 and self.last_battery >= 20:
                        self.speak_alert(f"Critical power warning. Battery is at {percent} percent. Please connect charger.")
                    
                    if plugged and percent == 100 and self.last_battery < 100:
                        self.speak_alert("Battery fully charged. You may disconnect power.")
                        
                    self.last_battery = percent

                # 2. SYSTEM HEALTH (CPU/RAM)
                cpu_usage = psutil.cpu_percent(interval=1)
                if cpu_usage > 90:
                    self.speak_alert("Warning. CPU usage is critically high. Cooling systems recommended.")

                # 3. TIME AWARENESS (The "Good Morning" Protocol)
                now = datetime.datetime.now()
                hour = now.hour
                
                # Reset greeting flag at midnight
                if hour == 0: self.greeted_morning = False
                
                # Trigger greeting between 7AM and 9AM
                if 7 <= hour < 9 and not self.greeted_morning:
                    self.speak_alert(f"Good morning, Sir. It is {now.strftime('%I:%M %p')}. Systems are fully operational.")
                    self.greeted_morning = True

            except Exception as e:
                print(f"Autonomy Error: {e}")
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)

# To test independently
if __name__ == "__main__":
    def mock_speak(text): print(f"SAYING: {text}")
    bot = AutonomyCore(mock_speak)
    bot.start()
    while True: time.sleep(1)