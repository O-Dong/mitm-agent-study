FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

COPY tool_server.py .

CMD ["python", "tool_server.py"]