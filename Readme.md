docker build --no-cache -t etl_pipeline . --progress=plain

docker run -it -v "$(pwd)/data:/app/data" etl_pipeline python src/extract.py


docker-compose up --build