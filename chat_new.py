# import following :
# 1.  pip install -q -U google-generativeai
# 2. pip install rich

# to get API KEY go to this link  (https://aistudio.google.com/app/apikey)
import google.generativeai as genai


gemini_key ='AIzaSyDpQKz3Rk9Xd45CYJBQQYzGeb49dE9iiR4'
genai.configure(api_key=gemini_key)


from rich.console import Console
from rich.text import Text

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Create a console object for rich output
console = Console()

def print_welcome_message():
    console.print("=" * 50, style="cyan")
    console.print("Welcome to the Chatbot!", style="cyan bold")
    console.print("Type your message and press Enter to chat.", style="yellow")
    console.print("Type 'exit' or 'quit' to end the chat.", style="yellow")
    console.print("=" * 50, style="cyan")

def format_response(user_input, bot_response):
    user_text = Text(f"You: {user_input}", style="green")
    bot_text = Text(f"Bot: {bot_response}", style="blue")
    return user_text, bot_text

# Display the welcome message
print_welcome_message()

while True:
    # Take input from the user
    prompt = console.input("[yellow]You: [/yellow]")
    
    # Check for exit condition
    if prompt.lower() in ['exit', 'quit']:
        console.print("Chat ended. Thank you for chatting!", style="cyan")
        break
    
    # Send the user's message to the chat model
    response = chat.send_message(prompt)
    
    # Print the formatted response
    user_text, bot_text = format_response(prompt, response.text)
    console.print(user_text)
    console.print(bot_text)