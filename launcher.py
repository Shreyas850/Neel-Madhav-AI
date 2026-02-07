import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import os
import sys
import logic_brain
import voice_core

# --- CONFIGURATION ---
# Base path handles the emoji 🦚 correctly
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

        # 1. Load Background (Krishna)
        self.bg_image = self.load_image(KRISHNA_PATH, (500, 750))
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 2. Load Orb (GIF Animation)
        self.orb_frames = self.load_gif(ORB_PATH, (150, 149))
        self.orb_label = tk.Label(root, bg="black", borderwidth=0)
        # Place Orb at bottom center
        self.orb_label.place(relx=0.5, rely=0.85, anchor="center")
        
        # Start Animation if frames exist
        if self.orb_frames:
            self.animate_orb(0)

        # 3. Status Label
        self.status_label = tk.Label(
            root, 
            text="Listening...", 
            font=("Helvetica", 16, "bold"), 
            fg="#00FF00",  # Green text
            bg="black"
        )
        self.status_label.place(relx=0.5, rely=0.05, anchor="center")

        # 4. Start Voice Thread
        self.start_thread()

    def load_image(self, path, size):
        """Loads a static image safely."""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            return None

    def load_gif(self, path, size):
        """Loads all frames of a GIF for animation."""
        frames = []
        try:
            gif = Image.open(path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize(size, Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
            return frames
        except Exception as e:
            print(f"⚠️ Orb GIF not found or error: {e}")
            return []

    def animate_orb(self, index):
        """Loops through GIF frames."""
        frame = self.orb_frames[index]
        self.orb_label.configure(image=frame)
        # 1000ms / 30fps = ~33ms delay
        self.root.after(33, self.animate_orb, (index + 1) % len(self.orb_frames))

    def update_status(self, text, color):
        """Updates the text label (Thread Safe)."""
        self.status_label.config(text=text, fg=color)

    def main_execution(self, text):
        """Callback when voice is heard."""
        if not text: return

        # 1. Change Status to SLEEPING (Busy)
        self.update_status("Sleeping (Thinking...)", "cyan")
        self.root.update_idletasks() # Force UI update immediately

        # 2. Process & Speak
        response = logic_brain.think(text)
        if response:
            print(f"🤖 Reply: {response}")
            logic_brain.speak_stream(response)
        
        # 3. Change Status back to LISTENING
        self.update_status("Listening...", "#00FF00")

    def start_thread(self):
        thread = threading.Thread(target=self.run_voice, daemon=True)
        thread.start()

    def run_voice(self):
        try:
            voice_core.listen_loop(self.main_execution)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    # Optional: Black background for the window itself
    root.configure(bg='black')
    
    app = NeelMadhavGUI(root)
    
    # Intro Sound
    logic_brain.speak_stream("Radhey Radhey")
    
    root.mainloop()