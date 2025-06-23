from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api-key', methods=['POST'])
def set_api_key():
    data = request.get_json(silent=True) or {}
    api_key = data.get('api_key')
    if not api_key:
        return jsonify({'error': 'API key missing'}), 400
    # Store the key securely in environment variable
    os.environ['CLAUDE_API_KEY'] = api_key
    return jsonify({'message': 'API key saved'})

@app.route('/test', methods=['GET'])
def test_connection():
    api_key = os.environ.get('CLAUDE_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not set'}), 400
    # In real use you would verify the key with the provider
    return jsonify({'message': 'Connection successful'})

@app.route('/claude', methods=['POST'])
def call_claude():
    api_key = os.environ.get('CLAUDE_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not set'}), 400
    data = request.get_json(silent=True) or {}
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'Prompt missing'}), 400
    # Placeholder for actual Claude API call
    completion = f"Echo: {prompt}"
    return jsonify({'completion': completion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
