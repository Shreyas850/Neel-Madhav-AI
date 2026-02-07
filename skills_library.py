import pywhatkit
import webbrowser
import pyautogui
import time
import os

def get_youtube_direct(song_name):
    """
    Finds the first video link for a song.
    """
    try:
        # PyWhatKit plays it instantly, we don't need to search manually
        print(f"🎵 Playing on YouTube: {song_name}")
        pywhatkit.playonyt(song_name)
        return True
    except Exception as e:
        print(f"Youtube Error: {e}")
        return False

def open_url(url):
    webbrowser.open(url)

def google_search(query):
    # We rename this so it is ONLY used when explicitly asked
    webbrowser.open(f"https://www.google.com/search?q={query}")

def capture_image():
    # Placeholder for vision
    return None