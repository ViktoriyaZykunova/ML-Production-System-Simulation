FROM python:3.9-slim

WORKDIR /app

#системные библиотеки для matplotlib (чтобы мог рисовать графики)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY plot/plot.py .

CMD ["python", "plot.py"]
