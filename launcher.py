import logic_brain
import voice_core 
import os
import sys
import threading
import cv2
import time

# --- 🦚 NEEL MADHAV GUI LAUNCHER 🦚 ---

# Global flag to control the system
is_running = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_execution(text):
    """
    This function runs in the background whenever Whisper hears something.
    """
    if not text: return

    # 1. Think (Process Command)
    response = logic_brain.think(text)
    
    # 2. Speak (Reply)
    if response:
        print(f"🤖 Reply: {response}")
        logic_brain.speak_stream(response)

def start_listening_thread():
    """Starts the listening loop in a separate thread so GUI doesn't freeze."""
    try:
        voice_core.listen_loop(main_execution)
    except Exception as e:
        print(f"❌ Listener Error: {e}")

if __name__ == "__main__":
    clear_screen()
    print("=========================================")
    print("   🦚 NEEL MADHAV AI (GUI EDITION) 🦚   ")
    print("=========================================")
    
    # 1. Start the Voice Listener in the Background
    listener_thread = threading.Thread(target=start_listening_thread, daemon=True)
    listener_thread.start()

    # 2. Start the GUI Window (Must be on Main Thread)
    # Make sure you have an image at this path!
    image_path = "static/krishna.jpg" 
    
    if not os.path.exists(image_path):
        print(f"⚠️ Warning: Image not found at {image_path}. GUI will be blank.")
        # Create a blank black image if file is missing
        import numpy as np
        image = np.zeros((500, 500, 3), dtype=np.uint8)
    else:
        image = cv2.imread(image_path)
        # Optional: Resize if too big
        image = cv2.resize(image, (800, 600)) 

    print("✅ GUI Started. Press 'q' in the window to quit.")
    
    # Optional: Intro Greeting
    logic_brain.speak_stream("Radhey Radhey")

    # 3. Keep the Window Open
    while is_running:
        cv2.imshow("Neel Madhav AI", image)
        
        # Press 'q' to close
        if cv2.waitKey(100) & 0xFF == ord('q'):
            print("\n👋 Closing System...")
            is_running = False
            break

    cv2.destroyAllWindows()
    sys.exit()