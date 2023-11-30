# Usar uma imagem oficial do Python como base
FROM python:3.8

# Definir o diretório de trabalho dentro do container
WORKDIR /app
ENV PYTHONPATH=/app

# Copiar os arquivos 'requirements.txt' e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
