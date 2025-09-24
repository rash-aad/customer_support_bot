# app.py

from flask import Flask, request, jsonify, render_template
from support_bot_agent import SupportBotAgent

# --- INITIALIZATION ---
print("Initializing SupportBotAgent for the API...")
bot = SupportBotAgent(document_path="data/faq.txt")
# Simple in-memory storage for the last context
# In a real app, this would be a proper session database
last_context = {"user": ""} 
print("Bot initialized and ready to serve requests.")

app = Flask(__name__)

# --- ROUTES ---
@app.route('/')
def home():
    """Serves the front-end HTML page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """API endpoint to get an initial answer."""
    global last_context
    data = request.json
    user_query = data.get('message')

    if not user_query:
        return jsonify({"error": "Request must include a 'message'."}), 400

    # We need the context to potentially provide more detail later
    context, score = bot._find_relevant_section(user_query)
    last_context['user'] = context # Save the context
    
    # Get the initial, short answer
    response = bot.answer_query(user_query)
    
    return jsonify({"response": response})

@app.route('/more_detail', methods=['GET'])
def more_detail():
    """API endpoint to get the full context for the last query."""
    global last_context
    return jsonify({"response": last_context.get('user', "No context available.")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)