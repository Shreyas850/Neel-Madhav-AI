from flask import Flask, request, jsonify
import logic_brain
import threading

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """API Endpoint to talk to Jarvis v6"""
    data = request.json
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # Send to the v6 Brain
    response = logic_brain.think(user_input)
    
    return jsonify({
        "response": response,
        "engine": "Jarvis v6 Custom Core"
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Online", "model": "jarvis_v6.gguf"})

def run_server():
    # Runs on http://127.0.0.1:5000
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    print("🚀 Starting Jarvis API Server...")
    run_server()