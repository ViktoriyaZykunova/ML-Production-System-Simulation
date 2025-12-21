FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ВАЖНО: путь из корня контекста (.) к файлу
COPY model/model.py .

CMD ["python", "model.py"]
