# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- AWS account with credentials
- Python 3.9+ (for local development)

## 5-Minute Setup

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your AWS credentials
nano .env
```

Required variables:
```
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

### 2. Deploy Services

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Deploy all services
./scripts/deploy-containers.sh
```

This will:
- Build Docker images
- Start PostgreSQL database
- Run ETL pipeline
- Train AI model
- Start prediction service
- Start Grafana dashboard

### 3. Verify Deployment

```bash
# Check service health
./scripts/health-check.sh

# View running services
docker-compose ps
```

### 4. Access Services

- **AI Prediction API**: http://localhost:8000
  - Health check: `curl http://localhost:8000/health`
  - Make prediction: 
    ```bash
    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"features": [1.0, 2.0, 3.0]}'
    ```

- **Grafana Dashboard**: http://localhost:3000
  - Username: admin
  - Password: admin

- **PostgreSQL Database**: localhost:5432
  - Database: smv_database
  - User: smv_user
  - Password: smv_password

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai_model_service
docker-compose logs -f etl_pipeline
docker-compose logs -f grafana
```

### Restart Services

```bash
# Restart specific service
docker-compose restart ai_model_service

# Restart all services
docker-compose restart
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Retrain Model

```bash
docker-compose --profile training run --rm ai_model_train
docker-compose restart ai_model_service
```

### Run ETL Pipeline Again

```bash
docker-compose run --rm etl_pipeline
```

## Troubleshooting

### Services Won't Start

1. Check if ports are available:
   ```bash
   lsof -i :5432  # PostgreSQL
   lsof -i :8000  # AI Model
   lsof -i :3000  # Grafana
   ```

2. Check Docker resources:
   ```bash
   docker system df
   docker system prune  # Clean up if needed
   ```

### ETL Pipeline Fails

1. Verify AWS credentials:
   ```bash
   aws s3 ls s3://your-bucket-name/
   ```

2. Check database connection:
   ```bash
   docker-compose exec postgres pg_isready
   ```

### Model Service Returns Errors

1. Check if model file exists:
   ```bash
   docker-compose exec ai_model_service ls -la /app/models/
   ```

2. Retrain model if missing:
   ```bash
   docker-compose --profile training run --rm ai_model_train
   ```

## Next Steps

- Read the full [documentation](./README.md)
- Configure AWS infrastructure for production deployment
- Customize the ETL pipeline for your data
- Adjust model parameters for your use case
- Set up monitoring alerts in Grafana

## Getting Help

If you encounter issues:
1. Check logs: `docker-compose logs [service-name]`
2. Run health check: `./scripts/health-check.sh`
3. Consult the full documentation
4. Open an issue on GitHub
