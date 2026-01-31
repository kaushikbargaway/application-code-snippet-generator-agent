# filename: app.py
# Backend for the AI Code Snippet Generator

import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

# --- 1. Initialization ---
app = Flask(__name__)

def initialize_client():
    """Initializes the Groq client from an environment variable."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set.")
        return None
    return Groq(api_key=api_key)

groq_client = initialize_client()

# --- 2. Core AI Logic ---
def generate_code_snippet(client, user_query):
    """Generates a code snippet using the Groq API."""
    if not client:
        return "Error: Groq client not initialized. Check API key."

    system_prompt = """
    You are an expert Python programming assistant. Your task is to generate a clean,
    efficient Python code snippet based on the user's request. Provide a brief,
    clear explanation of how the code works after the code block. Format your response in Markdown.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the Groq API: {e}"

# --- 3. Flask Routes ---
@app.route("/")
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route("/generate", methods=["POST"])
def generate():
    """API endpoint to handle code generation requests."""
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    response = generate_code_snippet(groq_client, user_query)
    return jsonify({"response": response})

# --- 4. Main Execution ---
if __name__ == "__main__":
    if groq_client is None:
        print("Could not start the application. Please set the GROQ_API_KEY environment variable.")
    else:
        app.run(debug=True) # debug=True helps with development