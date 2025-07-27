import torch
from flask import Flask, render_template, request, jsonify
import datetime
import os
from chatbot import MentalHealthChatbot



app = Flask(__name__)
try:
    chatbot = MentalHealthChatbot()
except Exception as e:
    print(f"Error initializing chatbot: {str(e)}")
    chatbot = None

# Simple logging function
def log_conversation(user_input, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - User: {user_input}\n{timestamp} - Bot: {bot_response}\n\n"
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Write to daily log file
    log_file = f"logs/conversation_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(log_file, 'a') as f:
        f.write(log_entry)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not chatbot:
        return jsonify({'response': "Chatbot is initializing, please wait..."})
    
    user_input = request.form['user_input']
    try:
        bot_response = chatbot.generate_response(user_input)
        log_conversation(user_input, bot_response)
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': "I'm still learning. Could you rephrase that?"})

if __name__ == '__main__':
    app.run(debug=True)

