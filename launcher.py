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

        # --- USE CANVAS FOR TRANSPARENCY (Fixes Black Boxes) ---
        self.canvas = tk.Canvas(root, width=500, height=750, highlightthickness=0, bg='black')
        self.canvas.pack(fill="both", expand=True)

        # 1. Draw Background Image
        self.bg_image = self.load_image(KRISHNA_PATH, (500, 750))
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            self.canvas.create_text(250, 375, text="Image Not Found", fill="white")

        # 2. Draw Status Text (Above Orb, No Box)
        # Position: x=250 (Center), y=580 (Above Orb)
        self.status_text_id = self.canvas.create_text(
            250, 580, 
            text="Initializing Brain...", 
            font=("Helvetica", 14, "bold"), # Sans-Serif Font
            fill="cyan"
        )

        # 3. Draw Orb (Bottom Center)
        # Position: x=250 (Center), y=680 (Bottom)
        self.orb_frames = self.load_gif(ORB_PATH, (150, 149))
        self.current_frame_idx = 0
        
        # Placeholder for orb on canvas
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
            # Iterator allows reading all frames of GIF
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA") # Use RGBA for transparency
                frame = frame.resize(size, Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
            return frames
        except Exception as e:
            print(f"⚠️ Orb GIF error: {e}")
            return []

    def animate_orb(self):
        if not self.orb_frames: return
        
        # Update the image item on the canvas
        frame = self.orb_frames[self.current_frame_idx]
        self.canvas.itemconfig(self.orb_image_id, image=frame)
        
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.orb_frames)
        self.root.after(33, self.animate_orb)

    def update_status(self, text, color):
        # Update the text item on the canvas
        self.canvas.itemconfig(self.status_text_id, text=text, fill=color)

    # --- BACKEND HANDLING ---
    def start_backend_thread(self):
        thread = threading.Thread(target=self.load_and_run_ai, daemon=True)
        thread.start()

    def load_and_run_ai(self):
        global logic_brain, voice_core
        try:
            print("🧠 [4/5] Importing AI Modules...")
            import logic_brain
            import voice_core
            print("✅ [5/5] AI Modules Loaded!")

            # Update Text to "Listening"
            self.root.after(0, lambda: self.update_status("Listening...", "#FFFFFF")) # White
            
            logic_brain.speak_stream("Radhey Radhey")
            voice_core.listen_loop(self.main_execution)

        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            self.root.after(0, lambda: self.update_status("System Error", "red"))

    def main_execution(self, text):
        if not text: return
        
        # Update UI to Thinking
        self.root.after(0, lambda: self.update_status("Thinking...", "cyan"))
        
        # Logic
        response = logic_brain.think(text)
        
        # Speak
        if response:
            print(f"🤖 Reply: {response}")
            logic_brain.speak_stream(response)
        
        # Reset UI
        self.root.after(0, lambda: self.update_status("Listening...", "#FFFFFF"))


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = NeelMadhavGUI(root)
        print("🖥️ GUI Loop Starting...")
        root.mainloop()
    except Exception as e:
        print(f"❌ LAUNCHER CRASHED: {e}")
        input("Press Enter...")