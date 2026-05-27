FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/

RUN pip install flask psycopg2-binary redis

CMD ["python", "app.py"]