# Dockerfile para UniAdvisor
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para banco de dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para iniciar
CMD ["python", "main.py"]
