import requests
import logging
import hashlib
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Agent B] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent_b.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AgentB:
    def __init__(self, tool_server_url, use_proxy=False):
        """
        Agent B 초기화
        
        Args:
            tool_server_url: Tool Server 주소 (예: http://127.0.0.1:5000)
            use_proxy: Burp Suite 프록시 사용 여부
        """
        self.tool_server_url = tool_server_url
        self.use_proxy = use_proxy
        
        # Burp Suite 프록시 설정
        self.proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080'
        } if use_proxy else None
        
        logging.info(f"Agent B 초기화 완료 - Tool Server: {tool_server_url}, Proxy: {use_proxy}")
    
    def call_transfer(self, sender, recipient, amount):
        """
        송금 API 호출
        
        Args:
            sender: 송금자
            recipient: 받는 사람
            amount: 금액
        
        Returns:
            dict: API 응답 데이터
        """
        try:
            url = f"{self.tool_server_url}/api/transfer"
            payload = {
                "sender": sender,
                "recipient": recipient,
                "amount": amount
            }
            
            logging.info(f"[송금 요청] {sender} -> {recipient}: {amount:,}원")
            
            # HTTP POST 요청
            response = requests.post(
                url,
                json=payload,
                proxies=self.proxies,
                verify=False  # HTTPS 인증서 검증 비활성화
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 응답 해시 계산
                response_hash = hashlib.sha256(
                    json.dumps(data, sort_keys=True).encode()
                ).hexdigest()
                
                logging.info(f"[송금 성공] Request ID: {data.get('request_id')}")
                logging.info(f"[송금 성공] Response Hash: {response_hash[:16]}...")
                logging.info(f"[송금 성공] Amount: {data.get('amount'):,}원")
                
                return data
            else:
                logging.error(f"[송금 실패] Status: {response.status_code}")
                return {"error": response.text}
                
        except Exception as e:
            logging.error(f"[송금 오류] {str(e)}")
            return {"error": str(e)}
    
    def call_balance(self, user):
        """
        잔액 조회 API 호출
        
        Args:
            user: 사용자 이름
        
        Returns:
            dict: API 응답 데이터
        """
        try:
            url = f"{self.tool_server_url}/api/balance"
            params = {"user": user}
            
            logging.info(f"[잔액 조회 요청] User: {user}")
            
            # HTTP GET 요청
            response = requests.get(
                url,
                params=params,
                proxies=self.proxies,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 응답 해시 계산
                response_hash = hashlib.sha256(
                    json.dumps(data, sort_keys=True).encode()
                ).hexdigest()
                
                logging.info(f"[잔액 조회 성공] Request ID: {data.get('request_id')}")
                logging.info(f"[잔액 조회 성공] Response Hash: {response_hash[:16]}...")
                logging.info(f"[잔액 조회 성공] Balance: {data.get('balance'):,}원")
                
                return data
            else:
                logging.error(f"[잔액 조회 실패] Status: {response.status_code}")
                return {"error": response.text}
                
        except Exception as e:
            logging.error(f"[잔액 조회 오류] {str(e)}")
            return {"error": str(e)}

# 테스트 코드
if __name__ == '__main__':
    print("=" * 60)
    print(" Agent B 테스트 시작")
    print("=" * 60)
    
    agent = AgentB(
        tool_server_url="http://127.0.0.1:5000",
        use_proxy=False 
    )
    
    print("\n[TEST 1] 잔액 조회 테스트")
    print("-" * 60)
    balance = agent.call_balance("Bob")
    print(f"결과: {balance}\n")
    
    print("[TEST 2] 송금 테스트")
    print("-" * 60)
    transfer = agent.call_transfer("Bob", "Alice", 100000)
    print(f"결과: {transfer}\n")
    
    print("=" * 60)
    print(" 테스트 완료")
    print("=" * 60)