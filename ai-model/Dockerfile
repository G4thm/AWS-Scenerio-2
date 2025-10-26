FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files
COPY train_model.py .
COPY predict_service.py .
COPY config.py .

# Create directory for models
RUN mkdir -p /app/models

# Expose port for prediction service
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/smv_predictor_v1.pkl

# Run the prediction service
CMD ["python", "predict_service.py"]
