from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

class MentalHealthChatbot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
        self.empathy_keywords = ["sad", "depressed", "anxious", "lonely", "stress", "stressed", "overwhelmed"]
        self.offensive_words = ["hate", "kill", "die", "stupid"]  # Add more as needed
    
    def contains_offensive_language(self, text):
        text_lower = text.lower()
        return any(word in text_lower for word in self.offensive_words)
    
    def needs_empathy(self, text):
        text_lower = text.lower()
        return any(word in text_lower for word in self.empathy_keywords)
    
    def get_empathy_response(self):
        empathy_responses = [
            "I'm really sorry you're feeling this way. It's okay to feel like this sometimes.",
            "That sounds really difficult. I'm here to listen if you want to talk more about it.",
            "I can hear that you're going through a tough time. Would you like to share more?",
            "Your feelings are valid. It's important to acknowledge them.",
            "I may not fully understand, but I care about how you're feeling."
        ]
        return random.choice(empathy_responses)
    
    def get_generic_response(self, user_input, chat_history_ids):
        new_user_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token, 
            return_tensors='pt'
        )
        
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
        
        chat_history_ids = self.model.generate(
            bot_input_ids, 
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        
        response = self.tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )
        
        return response, chat_history_ids
    
    def get_response(self, user_input, chat_history_ids=None):
        if self.contains_offensive_language(user_input):
            return "I'm sorry, but I can't engage with that kind of language. I'm here to help if you'd like to talk.", chat_history_ids
        
        if self.needs_empathy(user_input):
            return self.get_empathy_response(), chat_history_ids
            
        return self.get_generic_response(user_input, chat_history_ids)

if __name__ == "__main__":
    import random
    chatbot = MentalHealthChatbot()
    chat_history = None
    
    print("Mental Health Support Chatbot: Hi there. I'm here to listen if you'd like to talk about how you're feeling. (Type 'quit' to exit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        response, chat_history = chatbot.get_response(user_input, chat_history)
        print(f"Chatbot: {response}")



# Add to your MentalHealthChatbot class
CRISIS_KEYWORDS = ["suicide", "kill myself", "end my life", "want to die"]

def is_crisis_situation(self, text):
    text_lower = text.lower()
    return any(word in text_lower for word in self.CRISIS_KEYWORDS)

def get_crisis_response(self):
    return """I'm very concerned about what you're saying. Please know you're not alone.
    
Immediate help is available:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741 (US)
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

Would you like me to help you find local resources?"""