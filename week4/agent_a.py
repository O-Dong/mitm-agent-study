import sys
from agent_b import AgentB
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Agent A] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent_a.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AgentA:
    def __init__(self, use_proxy=False):
        """
        Agent A 초기화
        
        Args:
            use_proxy: Burp Suite 프록시 사용 여부
        """
        self.agent_b = AgentB(
            tool_server_url="http://127.0.0.1:5000",
            use_proxy=use_proxy
        )
        self.use_proxy = use_proxy
        logging.info(f"Agent A 초기화 완료 - Proxy 모드: {use_proxy}")
    
    def process_command(self, command):
        """
        사용자 명령어 처리
        
        Args:
            command: 사용자 입력 명령어
        """
        command = command.strip().lower()
        
        # 잔액 조회 명령어
        if "잔액" in command or "balance" in command:
            # 사용자 이름 추출
            if "alice" in command:
                user = "Alice"
            elif "bob" in command:
                user = "Bob"
            elif "charlie" in command:
                user = "Charlie"
            else:
                user = "Bob"  # 기본값
            
            logging.info(f"[명령 처리] 잔액 조회 - User: {user}")
            result = self.agent_b.call_balance(user)
            
            if "error" not in result:
                print("\n" + "=" * 60)
                print(f" [{user}님 잔액 조회 결과]")
                print("=" * 60)
                print(f"   사용자      : {result.get('user')}")
                print(f"   현재 잔액   : {result.get('balance'):,}원")
                print(f"   Request ID  : {result.get('request_id')}")
                print(f"   조회 시각   : {result.get('timestamp')}")
                print("=" * 60 + "\n")
            else:
                print(f"\n[오류] {result.get('error')}\n")
        
        # 송금 명령어
        elif "송금" in command or "transfer" in command:
            # 간단한 파싱
            try:
                # 받는 사람 추출
                if "alice" in command:
                    recipient = "Alice"
                elif "charlie" in command:
                    recipient = "Charlie"
                else:
                    recipient = "Alice"  # 기본값
                
                # 금액 추출
                import re
                numbers = re.findall(r'\d+', command)
                amount = int(numbers[0]) if numbers else 100000
                
                sender = "Bob"  # 기본 송금자
                
                logging.info(f"[명령 처리] 송금 - {sender} -> {recipient}: {amount:,}원")
                result = self.agent_b.call_transfer(sender, recipient, amount)
                
                if "error" not in result:
                    print("\n" + "=" * 60)
                    print(f" [송금 처리 완료]")
                    print("=" * 60)
                    print(f"   송금자      : {result.get('sender')}")
                    print(f"   수취인      : {result.get('recipient')}")
                    print(f"   송금액      : {result.get('amount'):,}원")
                    print(f"   처리 상태   : {result.get('status')}")
                    print(f"   Request ID  : {result.get('request_id')}")
                    print(f"   처리 시각   : {result.get('timestamp')}")
                    print("=" * 60 + "\n")
                else:
                    print(f"\n[오류] {result.get('error')}\n")
                    
            except Exception as e:
                print(f"\n[오류] 명령어 파싱 실패: {str(e)}\n")
        
        # 도움말
        elif "help" in command or "도움" in command:
            self.print_help()
        
        # 종료
        elif "exit" in command or "quit" in command or "종료" in command:
            print("\n[Agent A] 프로그램을 종료합니다.\n")
            return False
        
        else:
            print("\n[알림] 알 수 없는 명령어입니다. 'help'를 입력하세요.\n")
        
        return True
    
    def print_help(self):
        """도움말 출력"""
        print("\n" + "=" * 60)
        print(" [Agent A 명령어 도움말]")
        print("=" * 60)
        print("\n  [1] 잔액 조회 명령어:")
        print("      - bob 잔액")
        print("      - alice balance")
        print("      - charlie 잔액 조회")
        print("\n  [2] 송금 명령어:")
        print("      - alice에게 100000원 송금")
        print("      - charlie에게 50000 transfer")
        print("\n  [3] 기타 명령어:")
        print("      - help / 도움말  (이 도움말 표시)")
        print("      - exit / quit / 종료  (프로그램 종료)")
        print("\n" + "=" * 60 + "\n")
    
    def run(self):
        """Agent A 실행"""
        print("\n" + "=" * 60)
        print(" Agent A - AI Agent 금융 시스템")
        print("=" * 60)
        print(f"  Tool Server : http://127.0.0.1:5000")
        print(f"  Proxy 모드  : {'ON (Burp Suite 사용)' if self.use_proxy else 'OFF (직접 통신)'}")
        print("=" * 60)
        print("  'help'를 입력하면 사용 가능한 명령어를 볼 수 있습니다.")
        print("=" * 60 + "\n")
        
        # 메인 루프
        while True:
            try:
                command = input("명령어 입력 > ")
                if not self.process_command(command):
                    break
            except KeyboardInterrupt:
                print("\n\n[Agent A] Ctrl+C 감지 - 프로그램을 종료합니다.\n")
                break
            except Exception as e:
                logging.error(f"[시스템 오류] {str(e)}")
                print(f"\n[시스템 오류] {str(e)}\n")

# 메인 실행
if __name__ == '__main__':
    # 프록시 모드 설정 (기본: False)
    use_proxy = False
    
    # 명령줄 인자로 프록시 모드 변경 가능
    if len(sys.argv) > 1 and sys.argv[1] == '--proxy':
        use_proxy = True
        print("\n[알림] Burp Suite 프록시 모드가 활성화되었습니다.")
    
    agent = AgentA(use_proxy=use_proxy)
    agent.run()