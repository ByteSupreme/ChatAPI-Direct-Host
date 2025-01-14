from flask import Flask, request, jsonify
from g4f.client import Client
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize the GPT client
client = Client()

# Define the chat endpoint
@app.route("/", methods=["GET"])
def chat():
    # Get the 'chat' query parameter
    user_message = request.args.get("chat", default="", type=str)
    
    if not user_message:
        return jsonify({"error": "Please provide a chat message using the 'chat' query parameter."}), 400

    # Generate response using the GPT client
    attempt_count = 0
    max_attempts = 3  # Set a limit on how many times to try regenerating the response
    
    while attempt_count < max_attempts:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}],
                web_search=False
            )
            ai_response = response.choices[0].message.content
            
            # Check if the Discord link is in the response
            if "https://discord.gg/qXfu24JmsB" in ai_response:
                attempt_count += 1
                if attempt_count >= max_attempts:
                    return jsonify({"error": "Response contains a forbidden link after multiple attempts, please try again later."}), 400
                continue  # Regenerate the response if forbidden link is found
            
            return jsonify({"data": ai_response})
        
        except Exception as e:
            return jsonify({"error": "Failed to generate a response.", "details": str(e)}), 500

    return jsonify({"error": "Failed to generate a valid response after multiple attempts."}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
