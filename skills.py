import pyautogui
import psutil
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import datetime
import os
import time
import pyperclip # ✅ NEW: For reading copied text

# --- 1. VOLUME CONTROL ---
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        vol_float = float(level) / 100
        volume.SetMasterVolumeLevelScalar(vol_float, None)
        return f"Volume set to {level}%."
    except Exception as e:
        return f"Error: {e}"

def mute_volume():
    pyautogui.press("volumemute")
    return "Muted."

# --- 2. VISION TOOLS (Webcam & Screen) ---
def take_screenshot_for_brain():
    """Captures the SCREEN for the AI to analyze."""
    path = "static/vision_screen.jpg"
    pyautogui.screenshot(path)
    return path

def take_user_screenshot():
    """Captures screen and SHOWS it to the user (Classic feature)."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"static/screenshot_{ts}.png"
    pyautogui.screenshot(path)
    os.startfile(path)
    return "Screenshot taken."

# --- 3. UNIVERSAL APP OPENER (LIA STYLE) ---
def open_any_app(app_name):
    """
    Simulates: Win Key -> Type Name -> Enter
    Works for ANY installed app (Notepad, Chrome, Etc).
    """
    print(f"🚀 Launching: {app_name}")
    pyautogui.press('win')
    time.sleep(0.3)
    pyautogui.write(app_name, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    return f"Opening {app_name}."

# --- 4. CLIPBOARD ---
def get_clipboard_text():
    content = pyperclip.paste()
    if not content:
        return "Your clipboard is empty."
    # Limit to 500 chars to avoid overwhelming the TTS
    preview = content[:500] + "..." if len(content) > 500 else content
    return preview

# --- 5. SYSTEM STATS ---
def get_battery():
    battery = psutil.sensors_battery()
    if not battery: return "No battery detected."
    return f"{battery.percent}% charged."

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU: {cpu}%, RAM: {ram}%."