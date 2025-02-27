FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data/trusted
COPY src/ src/
COPY data/ data/
CMD ["bash", "-c", "python src/extract.py && python src/transform.py && python src/load.py"]