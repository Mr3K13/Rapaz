FROM python:3.11-slim

# Dependências do sistema necessárias para o mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libmysqlclient-dev \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
