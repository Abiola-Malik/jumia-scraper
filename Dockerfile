FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt || pip install -r requirements.txt
COPY . /app
CMD ["python3", "main.py"]