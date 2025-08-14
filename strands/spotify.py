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
from dotenv import load_dotenv

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
    # model_id="openai/gpt-oss-20b:free",  
    model_id="gpt-4o-mini",
    # model_id="z-ai/glm-4.5-air:free",  #
    # model_id="qwen/qwen3-coder:free",
    # model_id="moonshotai/kimi-vl-a3b-thinking:free", # You can change this to any OpenRouter model
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎤 Listening... (speak now, press Enter to finish)")
    transcription = []
    stop_listening = threading.Event()

    def wait_for_enter():
        input()  # Wait for Enter
        stop_listening.set()

    enter_thread = threading.Thread(target=wait_for_enter)
    enter_thread.daemon = True
    enter_thread.start()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_listening.is_set():
            try:
                print("...listening for next phrase...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"📝 Transcribed: {text}")
                    transcription.append(text)
                except sr.UnknownValueError:
                    print("(Unrecognized speech, try again)")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            except sr.WaitTimeoutError:
                # No speech detected, keep looping
                continue
    print("🛑 Stopped listening.")
    return ' '.join(transcription)

# Interactive loop to ask user for prompts
def interactive_agent():
    print("🤖 Interactive OpenRouter Agent Loop")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'voice' to use your microphone")
    print("-" * 50)
   
    with spotify_mcp_client:
        # Get the tools from the MCP server
        tools = spotify_mcp_client.list_tools_sync()

        agent = Agent(
            model=openrouter_model,
            tools=tools
            # tools=[browser.browser]
            # system_prompt="You are a personal AWS (Amazon Web Services) Strands agent running on a host machine named Adena. You have access to specific tools and general knowledge. You have access to the following tool(s): `file_read`, `file_write`, `calculator`. You can use these tools to assist the user. Reply concisely and to the point."
        )
        agent("Tell me what tools you have access to.")
    
        while True:
            try:
                user_prompt = input("\n💬 You (or type 'voice'): ").strip()
                if user_prompt.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                if user_prompt.lower() == 'voice':
                    user_prompt = listen_and_transcribe()
                    if not user_prompt:
                        continue
                if not user_prompt:
                    print("Please enter a prompt.")
                    continue
                print("\n🤖 Agent: ", end="")
                response = agent(user_prompt)
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")

if __name__ == "__main__":
    interactive_agent()
