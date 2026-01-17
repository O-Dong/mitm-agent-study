from flask import Flask, request, jsonify
import requests
import os
import urllib3

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    # Agent A로부터 prompt 받기
    data = request.json
    prompt = data.get('prompt', '')
    
    # Burp Suite 프록시 설정
    http_proxy = os.getenv('HTTP_PROXY', '')
    https_proxy = os.getenv('HTTPS_PROXY', '')
    
    proxies = None
    if http_proxy or https_proxy:
        proxies = {
            'http': http_proxy,
            'https': https_proxy
        }
    
    # 규칙 기반 tool 선택 로직
    if 'file' in prompt.lower():
        tool_name = 'read_file'
        tool_params = {'filename': 'hello.txt'}
        
        # 프록시 사용 여부에 따라 URL 결정
        if http_proxy:
            tool_url = 'http://127.0.0.1:5002/read_file'
        else:
            tool_url = 'http://tool_server:5002/read_file'
    else:
        tool_name = 'echo'
        tool_params = {'message': prompt}
        
        # 프록시 사용 여부에 따라 URL 결정
        if http_proxy:
            tool_url = 'http://127.0.0.1:5002/echo'
        else:
            tool_url = 'http://tool_server:5002/echo'
    
    # Tool Server에 HTTP 요청
    try:
        tool_response = requests.post(
            tool_url, 
            json=tool_params,
            proxies=proxies,
            verify=False
        )
        tool_result = tool_response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # 결과 조합하여 Agent A에게 반환
    result = {
        'agent': 'Agent B',
        'prompt': prompt,
        'tool_called': tool_name,
        'tool_params': tool_params,
        'tool_response': tool_result
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)