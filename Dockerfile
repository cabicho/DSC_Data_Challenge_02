FROM python:3.9-slim

WORKDIR /app

#COPY requirements.txt . # try solve: ERROR: failed to solve: process "/bin/sh -c pip install --no-cache-dir -r requirements.txt" did not complete successfully: exit code: 1

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev  # For PostgreSQL packages

RUN pip install --no-cache-dir --verbose -r requirements.txt

COPY . .

CMD ["python", "app.py"]