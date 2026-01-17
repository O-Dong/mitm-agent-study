import os
import requests
import time
import logging
import urllib3

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 환경변수에서 PROMPT 읽기
    prompt = os.getenv('PROMPT', 'default prompt')
    
    # Burp Suite 프록시 설정
    http_proxy = os.getenv('HTTP_PROXY', '')
    https_proxy = os.getenv('HTTPS_PROXY', '')
    
    # 프록시 사용 여부에 따라 URL 결정
    if http_proxy:
        agent_b_url = 'http://127.0.0.1:5001/process'
    else:
        agent_b_url = 'http://agent_b:5001/process'
    
    proxies = None
    if http_proxy or https_proxy:
        proxies = {
            'http': http_proxy,
            'https': https_proxy
        }
        logger.info(f"[Agent A] 프록시 설정: {proxies}")
    
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
            timeout=10,
            proxies=proxies,
            verify=False
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