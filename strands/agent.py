from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools.calculator import calculator
from strands_tools.file_read import file_read
from strands_tools.file_write import file_write
import os
import speech_recognition as sr
import threading
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

# Create an Ollama model instance
# ollama_model = OllamaModel(
#     host="http://localhost:11434",  # Ollama server address
#     model_id="qwen3:1.7b"               # Specify which model to use
# )

# agent = Agent(
#     model=ollama_model,
#     tools=[file_read, file_write, calculator],
#     system_prompt="You are a personal AWS (Amazon Web Services) Strands agent running on a host machine named Adena. You have access to specific tools and general knowledge. You have access to the following tool(s): `file_read`, `file_write`, `calculator`. You can use these tools to assist the user. Reply concisely and to the point."
# )

openai_model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o-mini",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

agent = Agent(
    model=openai_model,
    tools=[file_read, file_write, calculator]
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
    print("🤖 Interactive Agent Loop")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'voice' to use your microphone")
    print("-" * 50)
    
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