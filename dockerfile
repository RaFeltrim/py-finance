# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta usada pelo Streamlit
EXPOSE 8501

# Executa o app com Streamlit
CMD ["streamlit", "run", "dashboard_financeiro.py", "--server.port=8501", "--server.address=0.0.0.0"]
