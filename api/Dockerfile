FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./api/
RUN pip install --no-cache-dir -r api/requirements.txt

COPY . ./api/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "600", "--workers", "3", "api.app:create_app()"]
