# Predefined empathetic responses
BASIC_RESPONSES = {
    "greeting": [
        "Hello! How are you feeling today?",
        "Hi there. I'm here to listen. What's on your mind?",
        "Welcome. I'm ready to talk whenever you are."
    ],
    "stress": [
        "I'm sorry you're feeling stressed. Would you like to talk about what's bothering you?",
        "Stress can be overwhelming. Remember to take deep breaths.",
        "It's okay to feel stressed sometimes. You're not alone in this."
    ],
    "anxiety": [
        "Anxiety can be tough to deal with. Have you tried any relaxation techniques?",
        "I hear you. Anxiety can make things feel harder than they are.",
        "You're brave for sharing this. Would focusing on your breathing help right now?"
    ],
    "depression": [
        "I'm sorry you're feeling this way. You matter, and your feelings are valid.",
        "Depression can make everything feel heavy. Have you reached out to someone you trust?",
        "You're not alone in this, even if it feels that way sometimes."
    ],
    "default": [
        "I'm here to listen. Can you tell me more about how you're feeling?",
        "That sounds difficult. Would you like to elaborate?",
        "Thank you for sharing. How can I support you right now?"
    ]
}

# Offensive words filter
OFFENSIVE_WORDS = ["hate", "kill", "stupid", "idiot", "worthless"]  # Add more as needed

def contains_offensive_language(text):
    return any(word in text.lower() for word in OFFENSIVE_WORDS)