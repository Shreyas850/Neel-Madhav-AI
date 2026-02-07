import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import logic_brain
import voice_core
import os

ctk.set_appearance_mode("Dark")

class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ✅ WINDOW SETUP
        self.geometry("500x750") 
        self.title("NEEL MADHAV 🦚") 
        self.resizable(False, False)

        # ✅ CANVAS
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ✅ BACKGROUND
        # Ensure you have 'krishna.jpg' in static folder
        self.bg_path = os.path.join("static", "krishna.jpg") 
        self.bg_image_raw = None
        self.bg_image_ref = None 
        
        if os.path.exists(self.bg_path):
            self.bg_image_raw = Image.open(self.bg_path)
        else:
            print(f"⚠️ Warning: {self.bg_path} not found.")

        # ✅ ORB SETUP
        self.orb_frames = []
        self.orb_path = os.path.join("static", "orb.gif")
        if os.path.exists(self.orb_path):
            orb_gif = Image.open(self.orb_path)
            for frame in ImageSequence.Iterator(orb_gif):
                frame = frame.resize((140, 140), Image.Resampling.LANCZOS).convert("RGBA")
                self.orb_frames.append(ImageTk.PhotoImage(frame))

        self.bg_id = self.canvas.create_image(0, 0, anchor="nw")
        if self.orb_frames:
            self.orb_id = self.canvas.create_image(0, 0, image=self.orb_frames[0], anchor="center")
        
        # Text Layer
        self.text_id = self.canvas.create_text(
            0, 0, text="", fill="white", font=("Segoe UI", 14, "bold"), width=460, justify="center"
        )

        self.bind("<Configure>", self.resize_layout)
        self.current_frame = 0
        self.animate_orb()
        threading.Thread(target=self.start_brain_thread, daemon=True).start()

    def resize_layout(self, event):
        new_width = event.width
        new_height = event.height
        
        if self.bg_image_raw:
            resized_img = self.bg_image_raw.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_image_ref = ImageTk.PhotoImage(resized_img)
            self.canvas.itemconfig(self.bg_id, image=self.bg_image_ref)

        center_x = new_width // 2
        orb_y = new_height - 75 
        text_y = orb_y - 90 

        if self.orb_frames:
            self.canvas.coords(self.orb_id, center_x, orb_y)
        self.canvas.coords(self.text_id, center_x, text_y)
        self.canvas.tag_lower(self.bg_id)

    def animate_orb(self):
        if self.orb_frames:
            self.current_frame = (self.current_frame + 1) % len(self.orb_frames)
            self.canvas.itemconfig(self.orb_id, image=self.orb_frames[self.current_frame])
        self.after(60, self.animate_orb) 

    def start_brain_thread(self):
        # ✅ KRISHNA GREETING (Male)
        # "Radhe Radhe Sakha! Main Neel Madhav hoon."
        greeting = "राधे राधे सखा! मैं नील माधव हूँ। मैं आपकी क्या सहायता कर सकता हूँ?" 
        
        logic_brain.speak_stream(greeting)
        
        self.safe_update("Listening...")
        voice_core.listen_loop(self.handle_input)

    def handle_input(self, text):
        print(f"🎤 Heard: {text}")
        self.safe_update("Thinking...")
        try:
            response = logic_brain.think(text)
            print(f"🤖 Reply: {response}")
            logic_brain.speak_stream(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            self.safe_update("Error")
        self.safe_update("Listening...")

    def safe_update(self, text):
        self.after(0, lambda: self.canvas.itemconfig(self.text_id, text=text))

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()