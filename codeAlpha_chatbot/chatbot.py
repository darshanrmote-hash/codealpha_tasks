import os
import sys
import random
from datetime import datetime

# Predefined lists of responses for different categories
GREETING_RESPONSES = [
    "Hi there! How can I help you today? 😊",
    "Hello! Great to meet you. What's on your mind?",
    "Hey! I'm here and ready to chat. Ask me anything!"
]

STATUS_RESPONSES = [
    "I'm fine, thanks for asking! How are you doing? 🚀",
    "I am doing great! Ready to tackle some tasks.",
    "Doing wonderful, thanks! Hope you are having a fantastic day."
]

JOKES = [
    "Why do programmers wear glasses? Because they can't C#! 🤓",
    "There are 10 types of people in the world: those who understand binary, and those who don't. 💻",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
    "Why did the computer go to the doctor? Because it had a virus! 🦠",
    "A SQL query goes into a bar, walks up to two tables and asks, 'Can I join you?' 📊"
]

HELP_MESSAGE = """
I am AlphaBot, a rule-based AI chatbot. Here are some things you can ask me:
- Greet me (e.g., 'hello', 'hi', 'hey')
- Ask how I am (e.g., 'how are you', 'how is it going')
- Ask for a joke (e.g., 'tell me a joke', 'joke')
- Ask for my identity (e.g., 'what is your name', 'who are you')
- Ask for the current time/date (e.g., 'time', 'date')
- Ask for help (e.g., 'help', 'what can you do')
- Say goodbye (e.g., 'bye', 'goodbye', 'exit', 'quit')
"""

def clear_screen():
    """Clears the terminal screen for a clean user interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time():
    """Returns the formatted current time and date."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")

def clean_input(user_input):
    """
    Cleans the user input by converting to lowercase, stripping whitespace,
    and removing common punctuation.
    """
    user_input = user_input.lower().strip()
    # Remove basic punctuation
    for char in [".", ",", "!", "?", "'", '"']:
        user_input = user_input.replace(char, "")
    return user_input

def get_bot_response(user_input):
    """
    Determines the chatbot's response based on rule-matching of the user's input.
    """
    cleaned = clean_input(user_input)
    
    # Rule 1: Greetings
    if cleaned in ["hello", "hi", "hey", "greetings", "yo", "sup"]:
        return random.choice(GREETING_RESPONSES)
    
    # Rule 2: Status Check
    elif cleaned in ["how are you", "hows it going", "how are you doing", "how do you do", "how is it going"]:
        return random.choice(STATUS_RESPONSES)
    
    # Rule 3: Identity Check
    elif cleaned in ["what is your name", "who are you", "your name"]:
        return "My name is AlphaBot! I am your friendly rule-based virtual assistant. 🤖"
    
    # Rule 4: Capabilities / Help
    elif cleaned in ["help", "what can you do", "commands", "info"]:
        return HELP_MESSAGE.strip()
    
    # Rule 5: Tell a Joke
    elif "joke" in cleaned or "tell me a joke" in cleaned:
        return f"Here is a joke for you:\n{random.choice(JOKES)}"
    
    # Rule 6: Current Time
    elif cleaned in ["time", "date", "what time is it", "whats the date", "what is the date"]:
        return f"The current time is: {get_current_time()}"
    
    # Rule 7: Gratitude
    elif cleaned in ["thank you", "thanks", "thank you so much", "thank you!"]:
        return "You're very welcome! Let me know if you need anything else. 👍"
    
    # Rule 8: Agreement / Fine state
    elif cleaned in ["im good", "im fine", "doing good", "good", "fine", "great"]:
        return "That's wonderful to hear! 😊"
    
    # Rule 9: Farewell (Handled in main loop as well, but good to have here)
    elif cleaned in ["bye", "goodbye", "exit", "quit", "see you later"]:
        return "Goodbye! Have a great day! 👋"
    
    # Default Fallback rule
    else:
        return "I'm sorry, I didn't quite catch that. Type 'help' to see what I can do! 🤖"

def main():
    """Main execution loop for the Chatbot."""
    clear_screen()
    print("=" * 60)
    print("              Welcome to CodeAlpha Chatbot!              ")
    print("=" * 60)
    print("  Hi! I am AlphaBot. Let's chat!")
    print("  Type 'help' to see what I can do, or 'bye' to exit.")
    print("=" * 60)
    print()

    while True:
        try:
            # Prompt the user for input
            user_input = input("You: ")
            
            # Check if user wants to exit
            cleaned = clean_input(user_input)
            if cleaned in ["bye", "goodbye", "exit", "quit"]:
                print(f"AlphaBot: {get_bot_response(user_input)}")
                print("=" * 60)
                break
            
            # Print bot response
            response = get_bot_response(user_input)
            print(f"AlphaBot: {response}")
            print()
            
        except (KeyboardInterrupt, EOFError):
            print("\nAlphaBot: Goodbye! Have a great day! 👋")
            print("=" * 60)
            break

if __name__ == "__main__":
    main()
