import requests
import json
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_tool_request():
    # Agent B의 주소 (Docker 네트워크 내에서 컨테이너 이름으로 접근)
    url = "http://agent_b:8000/tool"
    
    # 전송할 JSON 데이터
    payload = {
        "tool": "read_file",
        "args": {
            "path": "/hello.txt"
        }
    }
    
    try:
        logger.info(f"요청 전송: tool='{payload['tool']}' args={payload['args']}")
        
        # HTTP POST 요청 전송
        response = requests.post(url, json=payload, timeout=5)
        
        # 응답 확인
        if response.status_code == 200:
            logger.info(f"서버 응답: {response.json()}")
        else:
            logger.error(f"오류 발생: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"연결 실패: {e}")

if __name__ == "__main__":
    # Agent B가 완전히 시작될 때까지 대기
    logger.info("Agent B 시작 대기 중...")
    time.sleep(3)
    
    # 요청 전송
    send_tool_request()
    
    logger.info("작업 완료")