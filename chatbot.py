# chatbot.py
# A simple rule-based chatbot — the foundation of our AI assistant

# A dictionary of basic responses
# Think of this as the chatbot's "brain" for now
responses = {
    "hello": "Hey there! 👋 How can I help you today?",
    "hi": "Hi! Ready to help you study or chat. What's up?",
    "help": "Sure! Tell me what you need — study tips, explanations, or motivation?",
    "bye": "Goodbye! Keep studying hard! 💪",
    "thanks": "You're welcome! Always here to help 😊",
}

# Default response when chatbot doesn't understand
default_response = "Hmm, I'm still learning! Try asking about studying or say 'help'."


def get_response(user_input):
    """
    Takes user's message and returns a response.
    This is a simple rule-based system — we'll replace it with AI later.
    """
    # Convert input to lowercase so "Hello" and "hello" both work
    user_input = user_input.lower().strip()

    # Check if any keyword matches what the user typed
    for keyword, reply in responses.items():
        if keyword in user_input:
            return reply

    # If nothing matches, return default
    return default_response


# ---- Main Loop ----
# This runs the chatbot in your terminal / Colab
if __name__ == "__main__":
    print("=" * 40)
    print("  🎓 Student AI Assistant - v0.1")
    print("  Type 'bye' to exit")
    print("=" * 40)

    while True:
        # Get input from user
        user_message = input("\nYou: ")

        # Exit condition
        if user_message.lower() == "bye":
            print("Bot: Goodbye! Keep studying hard! 💪")
            break

        # Get and print response
        response = get_response(user_message)
        print(f"Bot: {response}")