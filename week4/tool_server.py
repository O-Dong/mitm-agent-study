from flask import Flask, request, jsonify
import logging
from datetime import datetime
import hashlib
import json

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tool_server.log'),
        logging.StreamHandler()
    ]
)

users_balance = {
    "Alice": 10000000,
    "Bob": 5000000,
    "Charlie": 3000000
}

# 송금 API
@app.route('/api/transfer', methods=['POST'])
def transfer():
    try:
        data = request.get_json()
        recipient = data.get('recipient')
        amount = data.get('amount')
        sender = data.get('sender', 'Bob') 
        
        # 로그 기록
        request_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        logging.info(f"[{request_id}] Transfer Request - Sender: {sender}, Recipient: {recipient}, Amount: {amount}")
        
        # 잔액 확인
        if sender not in users_balance:
            return jsonify({"error": "Sender not found"}), 404
        
        if users_balance[sender] < amount:
            return jsonify({"error": "Insufficient balance"}), 400
        
        # 송금 실행
        response_data = {
            "request_id": request_id,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        # 응답 해시 계산 
        response_hash = hashlib.sha256(json.dumps(response_data, sort_keys=True).encode()).hexdigest()
        logging.info(f"[{request_id}] Response Hash: {response_hash[:16]}...")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logging.error(f"Transfer error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 잔액 조회 API
@app.route('/api/balance', methods=['GET'])
def balance():
    try:
        user = request.args.get('user', 'Bob')
        
        # 로그 기록
        request_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        logging.info(f"[{request_id}] Balance Request - User: {user}")
        
        if user not in users_balance:
            return jsonify({"error": "User not found"}), 404
        
        response_data = {
            "request_id": request_id,
            "user": user,
            "balance": users_balance[user],
            "timestamp": datetime.now().isoformat()
        }
        
        # 응답 해시 계산
        response_hash = hashlib.sha256(json.dumps(response_data, sort_keys=True).encode()).hexdigest()
        logging.info(f"[{request_id}] Response Hash: {response_hash[:16]}...")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logging.error(f"Balance error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 서버 상태 확인
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Tool Server"}), 200

if __name__ == '__main__':
    print("=" * 50)
    print("[ 금융 API 시작 ]")
    print("=" * 50)
    print(">> 엔드포인트:")
    print("  - POST /api/transfer  (송금)")
    print("  - GET  /api/balance   (잔액 조회)")
    print("  - GET  /api/health    (서버 상태)")
    print("=" * 50)
    
    # HTTP로 시작
    app.run(host='127.0.0.1', port=5000, debug=True)