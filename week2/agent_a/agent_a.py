import os
import requests
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 환경변수에서 PROMPT 읽기
    prompt = os.getenv('PROMPT', 'default prompt')
    agent_b_url = os.getenv('AGENT_B_URL', 'http://agent_b:5001/process')
    
    logger.info(f"[Agent A] 시작")
    logger.info(f"[Agent A] PROMPT: {prompt}")
    
    # Agent B가 준비될 때까지 대기
    logger.info("[Agent A] Agent B 시작 대기 중...")
    time.sleep(3)
    
    # Agent B에게 HTTP POST 요청
    try:
        logger.info(f"[Agent A] Agent B에게 요청 전송...")
        
        response = requests.post(
            agent_b_url,
            json={'prompt': prompt},
            timeout=10
        )
        
        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            logger.info(f"[Agent A] Agent B 응답 받음:")
            logger.info(f"  - Tool 호출: {result.get('tool_called')}")
            logger.info(f"  - Tool 파라미터: {result.get('tool_params')}")
            logger.info(f"  - Tool 결과: {result.get('tool_response')}")
        else:
            logger.error(f"[Agent A] 오류 발생: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"[Agent A] 연결 실패: {e}")
    
    logger.info("[Agent A] 작업 완료")

if __name__ == '__main__':
    main()