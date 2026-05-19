FROM python:3.11-slim

WORKDIR /app

# Gerekli derleyicileri kuruyoruz
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Kütüphaneleri önbelleksiz temiz kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
