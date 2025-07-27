from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from .responses import BASIC_RESPONSES, contains_offensive_language
import random

class MentalHealthChatbot:
    def __init__(self):
        # Initialize with a small pre-trained model
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.chat_history_ids = None
        
        # For simple responses when we don't use the model
        self.emotion_keywords = {
            "stress": ["stressed", "overwhelmed", "pressure"],
            "anxiety": ["anxious", "nervous", "panic"],
            "depression": ["depressed", "sad", "hopeless"]
        }

    def generate_response(self, user_input):
        # First check for offensive language
        if contains_offensive_language(user_input):
            return "I'm here to support you in a positive way. Could you rephrase that?"
        
        # Check for basic emotions
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return random.choice(BASIC_RESPONSES[emotion])
        
        # Check for greetings
        if any(greeting in user_input.lower() for greeting in ["hi", "hello", "hey"]):
            return random.choice(BASIC_RESPONSES["greeting"])
        
        # If no specific emotion detected, use the model or default response
        if len(user_input.split()) > 5:  # If input is long enough for model
            return self._generate_model_response(user_input)
        else:
            return random.choice(BASIC_RESPONSES["default"])
    
    def _generate_model_response(self, user_input):
        # Encode the new user input
        new_user_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token, 
            return_tensors='pt'
        )
        
        # Append to the chat history
        bot_input_ids = new_user_input_ids if self.chat_history_ids is None else torch.cat(
            [self.chat_history_ids, new_user_input_ids], dim=-1
        )
        
        # Generate response
        self.chat_history_ids = self.model.generate(
            bot_input_ids, 
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        
        # Decode and return response
        return self.tokenizer.decode(
            self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )