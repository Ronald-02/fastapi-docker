FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi fastapi-pagination
RUN pip install sqlalchemy
RUN pip install "sqlalchemy[asyncio]" asyncpg



COPY . .

CMD ["sh", "-c", "python create_tables.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
