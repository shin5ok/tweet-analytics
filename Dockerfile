FROM python:3.9-slim

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "-b 0.0.0.0:8080", "main:app", "-t 600"]
ENV PYTHONUNBUFFERED 1