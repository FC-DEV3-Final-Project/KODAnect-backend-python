FROM python:3.12 AS dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.12-slim AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
 build-essential gcc libpq-dev curl git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y --auto-remove gcc build-essential libpq-dev git \
 && rm -rf /root/.cache /root/.local

COPY . .

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--workers=1", "--timeout=30", "--bind", "0.0.0.0:8000"]
