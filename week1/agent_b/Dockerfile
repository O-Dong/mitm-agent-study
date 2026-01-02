# Python 3.12 이미지를 베이스로 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt를 컨테이너로 복사
COPY requirements.txt .

# 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드를 컨테이너로 복사
COPY tool_server.py .

# 8000번 포트 오픈
EXPOSE 8000

# 컨테이너 시작 시 실행할 명령
CMD ["python", "tool_server.py"]