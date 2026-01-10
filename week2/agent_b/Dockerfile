FROM python:3.9-slim

WORKDIR /app

RUN pip install flask requests

COPY agent_b.py .

CMD ["python", "agent_b.py"]