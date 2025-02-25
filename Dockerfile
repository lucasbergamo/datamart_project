# Usar imagem oficial do Python
FROM python:3.9-slim

# Definir diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar arquivos do projeto para dentro do contêiner
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/

# Comando para rodar os scripts de extração, transformação e carga
CMD ["bash", "-c", "python src/extract.py && python src/transform.py && python src/load.py"]
