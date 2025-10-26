#!/bin/bash
set -e

echo "=========================================="
echo "SMV Containers Deployment Script"
echo "=========================================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Error: docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Error: docker-compose is required but not installed."; exit 1; }

# Navigate to project root
cd "$(dirname "$0")/.."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please copy .env.example and configure it."
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your AWS credentials before continuing."
    exit 1
fi

echo "Building Docker images..."
docker-compose build

echo "Starting PostgreSQL database..."
docker-compose up -d postgres

echo "Waiting for PostgreSQL to be ready..."
sleep 10

echo "Running ETL pipeline..."
docker-compose run --rm etl_pipeline

echo "Training AI model..."
docker-compose --profile training run --rm ai_model_train

echo "Starting AI prediction service..."
docker-compose up -d ai_model_service

echo "Starting Grafana monitoring dashboard..."
docker-compose up -d grafana

echo ""
echo "=========================================="
echo "All services deployed successfully!"
echo "=========================================="
echo ""
echo "Service URLs:"
echo "- AI Prediction API: http://localhost:8000"
echo "- Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "- PostgreSQL: localhost:5432"
echo ""
echo "To check service status:"
echo "  docker-compose ps"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f [service-name]"
echo ""
echo "To stop all services:"
echo "  docker-compose down"
