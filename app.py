import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up Google API Key securely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing! Please add it to the .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variables to store conversation history
conversation_history = []

# Voice assistance function
def voice_assistance(user_input):
    global conversation_history

    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. The user just asked:
    '{user_input}'
    Provide a clear and concise response while keeping the conversation engaging.
    """

    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({'user': user_input, 'ai': response})

    return response

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to process voice input
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistance(user_input)

    return jsonify({'response': response, 'conversation_history': conversation_history})

if __name__ == '__main__':
    app.run(debug=True)
