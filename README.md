# Build the Docker image

docker build -t invoice-ocr-app .

# Run the container, mounting your .env file

docker run -p 8501:8501 -v /path/to/your/.env:/app/.env invoice-ocr-app

tesseract
poppler
