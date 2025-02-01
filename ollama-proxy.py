import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

def remove_think_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    for think_tag in soup.find_all('think'):
        think_tag.decompose()
    return str(soup)

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def process_request():
    api_key = os.getenv('OLLAMA_API_KEY')
    host = os.getenv('OLLAMA_SERVER', 'http://localhost:11434')

    # Check if Content-Type is application/json
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    try:
        response = requests.post(
            url=f"{host}/api/chat",
            json=request.get_json(),
            # headers={'Authorization': f'Ola-Api-Key {api_key}'}
            headers=request.headers
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to process request'}), response.status_code
        
        # Remove <think> tags from the response
        response_data = response.json()
        if 'message' in response_data and 'content' in response_data['message'] and isinstance(response_data['message']['content'], str):
            filtered_text = remove_think_tags(response_data['message']['content'])
            response_data['message']['content'] = filtered_text

        return jsonify(response_data), 200

    except requests.exceptions.RequestException as e:
        print(f"Request to Ollama endpoint /api/chat failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    api_key = os.getenv('OLLAMA_API_KEY')
    host = os.getenv('OLLAMA_SERVER', 'http://localhost:11434')

    try:
        # Forward the request to the Ollama server
        response = requests.request(
            method=request.method,
            url=f"{host}/{path}",
            headers={
                'Authorization': f'Ola-Api-Key {api_key}',
                **request.headers
            },
            data=request.get_data()
        )

        # Return the response from the Ollama server as-is
        return response.content, response.status_code, response.headers.items()

    except requests.exceptions.RequestException as e:
        print(f"Request to Ollama endpoint /{path} failed: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = os.getenv('OLLAMA_PROXY_PORT', 11435)
    host = os.getenv('OLLAMA_PROXY_HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=True)