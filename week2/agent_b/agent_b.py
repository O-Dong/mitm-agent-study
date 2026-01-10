from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    
    # Agent A로부터 prompt 받기
    data = request.json
    prompt = data.get('prompt', '')
    
    print(f"[Agent B] 받은 prompt: {prompt}")
    
    # 규칙 기반 tool 선택 로직
    if 'file' in prompt.lower():
        # 'file' 키워드가 있으면 read_file 호출
        tool_name = 'read_file'
        tool_params = {'filename': 'hello.txt'}
        tool_url = 'http://tool_server:5002/read_file'
        
        print(f"[Agent B] 선택된 tool: read_file")
        
    else:
        # 그 외에는 echo 호출
        tool_name = 'echo'
        tool_params = {'message': prompt}
        tool_url = 'http://tool_server:5002/echo'
        
        print(f"[Agent B] 선택된 tool: echo")
    
    # Tool Server에 HTTP 요청
    try:
        tool_response = requests.post(tool_url, json=tool_params)
        tool_result = tool_response.json()
    except Exception as e:
        print(f"[Agent B] Tool Server 오류: {e}")
        return jsonify({'error': str(e)}), 500
    
    # 결과 조합하여 Agent A에게 반환
    result = {
        'agent': 'Agent B',
        'prompt': prompt,
        'tool_called': tool_name,
        'tool_params': tool_params,
        'tool_response': tool_result
    }
    
    print(f"[Agent B] 응답 전송: {result}")
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)