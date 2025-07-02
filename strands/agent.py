from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools.file_read import file_read
import os

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="llama2:7b"               # Specify which model to use
)

# Create an agent using the Ollama model
# Restrict file_read tool to the repo folder only
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def file_read_repo_only(tool_use, **kwargs):
    # Only allow reading files within the repo root
    input_path = tool_use.get('input', {}).get('path', '')
    # Support wildcards and relative paths
    abs_paths = [os.path.abspath(os.path.join(REPO_ROOT, p.strip())) for p in input_path.split(',')]
    for abs_path in abs_paths:
        if not abs_path.startswith(REPO_ROOT):
            return {
                'toolUseId': tool_use.get('file_read_repo_only', '1234567890'),
                'status': 'error',
                'content': [{'text': 'Access denied: Only files within the repo folder can be read.'}],
            }
    return file_read(tool_use, **kwargs)

agent = Agent(
    model=ollama_model,
    tools=[file_read],
    system_prompt="You are a personal AWS (Amazon Web Services) Strands agent running on a host machine named Adena. You have access to specific tools and general knowledge. You have access to the following tool(s): `file_read`. You can use these tools to assist the user. Reply concisely and to the point."
)
# Interactive loop to ask user for prompts
def interactive_agent():
    print("🤖 Interactive Agent Loop")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_prompt = input("\n💬 You: ").strip()
            
            # Check for exit commands
            if user_prompt.lower() in ['quit', 'exit', 'bye', 'q']:
                print("👋 Goodbye! Thanks for chatting!")
                break
            
            # Skip empty prompts
            if not user_prompt:
                print("Please enter a prompt.")
                continue
            
            # Get agent response
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