from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator
from strands_tools import file_read
from strands_tools import file_write
from strands_tools.mcp_client import MCPClient
from mcp import stdio_client, StdioServerParameters
# from strands_tools.browser import LocalChromiumBrowser

import os
import speech_recognition as sr
import threading
import time
from dotenv import load_dotenv
import pyttsx3

load_dotenv()

# For Windows - Spotify MCP Server:
spotify_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uv", 
        args=[
            "run", 
            "--directory", 
            "C:\\devl\\spotify-mcp", 
            "spotify-mcp"
        ],
        env={
            **os.environ,  # Include all current env vars
            'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID'),
            'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET'),
            'SPOTIFY_REDIRECT_URI': os.getenv('SPOTIFY_REDIRECT_URI'),
            'SPOTIPY_CLIENT_ID': os.getenv('SPOTIPY_CLIENT_ID'),
            'SPOTIPY_CLIENT_SECRET': os.getenv('SPOTIPY_CLIENT_SECRET')
        }
    )
))
# Create an OpenRouter model instance
openrouter_model = OpenAIModel(
    # client_args={
    #     "api_key": os.getenv("OPENROUTER_KEY"),
    #     "base_url": "https://openrouter.ai/api/v1",
    # },
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    # model_id="openai/gpt-oss-20b:free",  # no tool use
    # model_id="z-ai/glm-4.5-air:free",  # tool use!!!
    # model_id="qwen/qwen3-coder:free", # tool use!!!
    # model_id="moonshotai/kimi-vl-a3b-thinking:free", # no tool use
    model_id="gpt-4o-mini",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎤 Listening... (speak now, will auto-submit after 5 seconds of silence)")
    transcription = []
    stop_listening = threading.Event()
    last_speech_time = time.time()

    def auto_submit_timer():
        """Auto-submit after 5 seconds of silence"""
        while not stop_listening.is_set():
            time.sleep(0.5)  # Check every 0.5 seconds
            if time.time() - last_speech_time > 5.0:  # 5 seconds of silence
                if transcription:  # Only submit if we have some transcription
                    print("⏰ Auto-submitting after 5 seconds of silence...")
                    stop_listening.set()
                    break

    # Start the auto-submit timer
    timer_thread = threading.Thread(target=auto_submit_timer)
    timer_thread.daemon = True
    timer_thread.start()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_listening.is_set():
            try:
                print("...listening for next phrase...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"📝 Transcribed: {text}")
                    transcription.append(text)
                    last_speech_time = time.time()  # Update last speech time
                except sr.UnknownValueError:
                    print("(Unrecognized speech, continuing to listen...)")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            except sr.WaitTimeoutError:
                # No speech detected, keep looping
                continue
    print("🛑 Stopped listening.")
    return ' '.join(transcription)

def speak_text(text, rate=150):
    """
    Convert text to speech using pyttsx3
    Handles long responses by breaking into sentences for better TTS
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        
        # Clean up the text for better TTS
        text = str(text).strip()
        
        # If it's a very long response, break it into sentences
        if len(text) > 200:
            print(f"🔊 Speaking long response (breaking into sentences)...")
            # Split by common sentence endings and speak each part
            import re
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for i, sentence in enumerate(sentences):
                if sentence:
                    print(f"🔊 Speaking part {i+1}/{len(sentences)}: {sentence[:50]}...")
                    engine.say(sentence)
                    engine.runAndWait()
                    # Small pause between sentences
                    time.sleep(0.5)
        else:
            print(f"🔊 Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
            
    except Exception as e:
        print(f"❌ TTS Error: {e}")

# Interactive loop to ask user for prompts
def interactive_agent():
    print("🤖 Interactive OpenRouter Agent Loop")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'voice' to use your microphone (auto-submits after 5s silence)")
    print("Type 'speak <text>' to convert text to speech")
    print("Type 'tts on' or 'tts off' to toggle text-to-speech for agent responses")
    print("-" * 50)
    
    # TTS toggle - default to ON for full voice experience
    tts_enabled = True
   
    with spotify_mcp_client:
        # Get the tools from the MCP server
        tools = spotify_mcp_client.list_tools_sync()

        agent = Agent(
            model=openrouter_model,
            tools=tools
            # tools=[browser.browser]
            # system_prompt="You are a personal AWS (Amazon Web Services) Strands agent running on a host machine named Adena. You have access to specific tools and general knowledge. You have access to the following tool(s): `file_read`, `file_write`, `calculator`. You can use these tools to assist the user. Reply concisely and to the point."
        )
        
        # Initial agent response with TTS
        print("🤖 Agent: ", end="")
        response = agent("Tell me what tools you have access to.")
        if tts_enabled:
            speak_text(str(response))
    
        while True:
            try:
                user_prompt = input("\n💬 You (or type 'voice'): ").strip()
                if user_prompt.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                elif user_prompt.lower() == 'voice':
                    user_prompt = listen_and_transcribe()
                    if not user_prompt:
                        continue
                elif user_prompt.lower().startswith('speak '):
                    text_to_speak = user_prompt[6:]  # Remove 'speak ' prefix
                    speak_text(text_to_speak)
                    continue
                elif user_prompt.lower() == 'tts on':
                    tts_enabled = True
                    print("🔊 TTS enabled - Agent responses will be spoken")
                    speak_text("Text to speech is now enabled")
                    continue
                elif user_prompt.lower() == 'tts off':
                    tts_enabled = False
                    print("🔇 TTS disabled - Agent responses will be text only")
                    continue
                if not user_prompt:
                    print("Please enter a prompt.")
                    continue
                    
                print("\n🤖 Agent: ", end="")
                response = agent(user_prompt)
                
                # Automatically speak the agent's response if TTS is enabled
                if tts_enabled:
                    speak_text(str(response))
                    
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")

if __name__ == "__main__":
    interactive_agent()
