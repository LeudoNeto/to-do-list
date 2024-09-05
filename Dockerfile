# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar o requirements.txt e instalar as dependências do projeto
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para dentro do container
COPY . .

# Expor a porta usada pelo FastAPI
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn (servidor ASGI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
