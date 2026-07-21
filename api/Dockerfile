FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "600", "--workers", "3", "api.app:create_app()"]
