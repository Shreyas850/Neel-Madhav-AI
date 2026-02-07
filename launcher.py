import logic_brain
import voice_core 
import os
import sys

# --- 🦚 NEEL MADHAV LAUNCHER ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_execution(text):
    """
    This function is called whenever Whisper hears something.
    """
    if not text: return

    # 1. Think (Process Command)
    response = logic_brain.think(text)
    
    # 2. Speak (Reply)
    if response:
        print(f"🤖 Reply: {response}")
        logic_brain.speak_stream(response)

if __name__ == "__main__":
    clear_screen()
    print("=========================================")
    print("   🦚 NEEL MADHAV AI (GPU EDITION) 🦚   ")
    print("=========================================")
    
    # Optional: Startup Sound
    logic_brain.speak_stream("Radhey Radhey! Neel Madhav is ready.")

    try:
        # Start the Whisper Listening Loop (Infinite)
        voice_core.listen_loop(main_execution)
        
    except KeyboardInterrupt:
        print("\n👋 Closing Neel Madhav...")
        sys.exit()