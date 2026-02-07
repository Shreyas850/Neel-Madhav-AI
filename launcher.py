import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import os
import sys
import time

# --- DEBUG STARTUP ---
print("🚀 [1/5] Launcher script started...")

# Global variables for backend modules (Lazy Loaded)
logic_brain = None
voice_core = None

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
KRISHNA_PATH = os.path.join(STATIC_DIR, "krishna.jpg")
ORB_PATH = os.path.join(STATIC_DIR, "orb.gif")

class NeelMadhavGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Neel Madhav AI 🦚")
        self.root.geometry("500x750")
        self.root.resizable(False, False)

        print("🎨 [2/5] Initializing GUI elements...")

        # --- USE CANVAS FOR TRANSPARENCY ---
        self.canvas = tk.Canvas(root, width=500, height=750, highlightthickness=0, bg='black')
        self.canvas.pack(fill="both", expand=True)

        # 1. Background
        self.bg_image = self.load_image(KRISHNA_PATH, (500, 750))
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            self.canvas.create_text(250, 375, text="Image Not Found", fill="white")

        # 2. Status Text (Above Orb)
        self.status_text_id = self.canvas.create_text(
            250, 580, 
            text="Starting System...", 
            font=("Helvetica", 14, "bold"), 
            fill="cyan"
        )

        # 3. Orb (Bottom Center)
        self.orb_frames = self.load_gif(ORB_PATH, (150, 149))
        self.current_frame_idx = 0
        self.orb_image_id = self.canvas.create_image(250, 680, anchor="center")
        
        if self.orb_frames:
            self.animate_orb()

        # 4. Schedule Backend Loading
        print("⏳ [3/5] Scheduling backend load...")
        self.root.after(1000, self.start_backend_thread)

    def load_image(self, path, size):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"❌ Error loading image {path}: {e}")
            return None

    def load_gif(self, path, size):
        frames = []
        try:
            gif = Image.open(path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                frame = frame.resize(size, Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
            return frames
        except Exception as e:
            print(f"⚠️ Orb GIF error: {e}")
            return []

    def animate_orb(self):
        if not self.orb_frames: return
        frame = self.orb_frames[self.current_frame_idx]
        self.canvas.itemconfig(self.orb_image_id, image=frame)
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.orb_frames)
        self.root.after(33, self.animate_orb)

    def update_status(self, text, color):
        self.canvas.itemconfig(self.status_text_id, text=text, fill=color)

    # --- BACKEND HANDLING ---
    def start_backend_thread(self):
        thread = threading.Thread(target=self.load_and_run_ai, daemon=True)
        thread.start()

    def load_and_run_ai(self):
        global logic_brain, voice_core
        try:
            # STEP 1: LOAD BRAIN (Llama)
            self.root.after(0, lambda: self.update_status("Loading Brain (Phi-3)...", "yellow"))
            print("🧠 [4/5] Loading Logic Brain...")
            import logic_brain
            
            # STEP 2: LOAD EARS (Whisper)
            self.root.after(0, lambda: self.update_status("Loading Ears (Whisper)...", "orange"))
            print("👂 [4.5/5] Loading Voice Core...")
            import voice_core
            
            print("✅ [5/5] All Modules Loaded!")

            # STEP 3: READY
            self.root.after(0, lambda: self.update_status("Listening...", "#00FF00"))
            
            logic_brain.speak_stream("Radhey Radhey")
            voice_core.listen_loop(self.main_execution)

        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            self.root.after(0, lambda: self.update_status("System Error", "red"))

    def main_execution(self, text):
        if not text: return
        
        self.root.after(0, lambda: self.update_status("Thinking...", "cyan"))
        
        response = logic_brain.think(text)
        
        if response:
            print(f"🤖 Reply: {response}")
            logic_brain.speak_stream(response)
        
        self.root.after(0, lambda: self.update_status("Listening...", "#00FF00"))


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = NeelMadhavGUI(root)
        print("🖥️ GUI Loop Starting...")
        root.mainloop()
    except Exception as e:
        print(f"❌ LAUNCHER CRASHED: {e}")
        input("Press Enter...")