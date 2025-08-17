#!/usr/bin/env python3
"""
Text-to-Speech Examples using Python libraries
"""

import pyttsx3
import time

def tts_with_pyttsx3(text, voice_name=None, rate=150):
    """
    Convert text to speech using pyttsx3 (local, no internet required)
    
    Args:
        text (str): Text to convert to speech
        voice_name (str): Optional voice name to use
        rate (int): Speech rate (words per minute)
    """
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', rate)  # Speed of speech
        
        # List available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} ({voice.id})")
        
        # Set specific voice if requested
        if voice_name:
            for voice in voices:
                if voice_name.lower() in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    print(f"Using voice: {voice.name}")
                    break
        
        # Convert text to speech
        print(f"Speaking: '{text}'")
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Error with pyttsx3: {e}")

def tts_with_windows_sapi(text):
    """
    Windows-specific TTS using the built-in SAPI (Speech API)
    This is even more lightweight than pyttsx3
    """
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        print(f"Speaking: '{text}'")
        speaker.Speak(text)
    except ImportError:
        print("pywin32 not installed. Install with: pip install pywin32")
    except Exception as e:
        print(f"Error with Windows SAPI: {e}")

def tts_with_espeak(text):
    """
    TTS using eSpeak (if installed on system)
    """
    try:
        import subprocess
        print(f"Speaking: '{text}'")
        subprocess.run(['espeak', text], check=True)
    except FileNotFoundError:
        print("eSpeak not installed. Install from: http://espeak.sourceforge.net/")
    except Exception as e:
        print(f"Error with eSpeak: {e}")

def interactive_tts():
    """Interactive TTS demo"""
    print("🎤 Text-to-Speech Demo")
    print("=" * 30)
    
    while True:
        text = input("\nEnter text to speak (or 'quit' to exit): ").strip()
        
        if text.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if not text:
            continue
            
        print("\nChoose TTS method:")
        print("1. pyttsx3 (local)")
        print("2. Windows SAPI (Windows only)")
        print("3. eSpeak (if installed)")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            rate = input("Enter speech rate (default 150): ").strip()
            rate = int(rate) if rate.isdigit() else 150
            tts_with_pyttsx3(text, rate=rate)
        elif choice == '2':
            tts_with_windows_sapi(text)
        elif choice == '3':
            tts_with_espeak(text)
        else:
            print("Invalid choice, using pyttsx3...")
            tts_with_pyttsx3(text)

if __name__ == "__main__":
    # Example usage
    print("Testing TTS with pyttsx3...")
    tts_with_pyttsx3("Hello! This is a test of text to speech using Python.")
    
    print("\n" + "="*50)
    
    # Start interactive demo
    interactive_tts()
