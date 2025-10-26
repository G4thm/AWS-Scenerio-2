FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL scripts
COPY etl_script.py .
COPY config.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the ETL pipeline
CMD ["python", "etl_script.py"]
