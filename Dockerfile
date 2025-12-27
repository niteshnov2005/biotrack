# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g. tesseract for OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend
COPY public ./public
# Copy root python files needed path imports
COPY *.py .
# Copy database (for demo persistence within container, ephemeral)
COPY medical_assistant.db . 

# Expose port
EXPOSE 8080

# Environment variables
ENV PORT=8080

# Run command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
