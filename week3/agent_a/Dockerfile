FROM python:3.9-slim

WORKDIR /app

RUN pip install requests

COPY agent_a.py .

CMD ["python", "agent_a.py"]