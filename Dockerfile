# Usar uma imagem oficial do Python como base
FROM python:3.8

# Definir o diretório de trabalho dentro do container
WORKDIR /app
ENV PYTHONPATH=/app

# Copiar os arquivos 'requirements.txt' e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar debugpy
RUN pip install debugpy

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Comando para iniciar o servidor Uvicorn com recarga
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Comando para iniciar o servidor Uvicorn com suporte a debug
#CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "app/main.py"]
