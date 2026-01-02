from flask import Flask, request, jsonify
import logging

# Flask 앱 생성
app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /tool 엔드포인트 - POST 요청만 받음
@app.route('/tool', methods=['POST'])
def handle_tool():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 로그 출력
    logger.info(f"받은 요청: tool='{data.get('tool')}' args={data.get('args')}")
    
    # 응답 생성
    response = {
        'status': 'ok',
        'tool': data.get('tool'),
        'args': data.get('args')
    }
    
    # JSON 응답 반환
    return jsonify(response), 200

if __name__ == '__main__':
    # 0.0.0.0 = 모든 네트워크 인터페이스에서 접속 허용
    # port=8000 = 8000번 포트에서 대기
    app.run(host='0.0.0.0', port=8000, debug=True)