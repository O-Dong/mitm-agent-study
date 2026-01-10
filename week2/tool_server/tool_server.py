from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/read_file', methods=['POST'])
def read_file():
    """파일 읽기 tool"""
    data = request.json
    filename = data.get('filename', '')
    filepath = f'/data/{filename}'
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return jsonify({'status': 'success', 'content': content})
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'File not found'}), 404

@app.route('/echo', methods=['POST'])
def echo():
    """메시지 반환 tool"""
    data = request.json
    message = data.get('message', '')
    return jsonify({'status': 'success', 'echo': message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)