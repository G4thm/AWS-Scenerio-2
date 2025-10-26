# AWS Scenario 2: Cloud-Based Data Processing and AI Deployment

## Overview

This project implements a comprehensive cloud-based data processing and AI deployment infrastructure on AWS. The system includes:

- **smv_data-ai-node**: EC2 instance hosting data processing and AI services
- **smv_etl-pipeline**: Docker container for ETL operations (S3 → PostgreSQL)
- **smv_predictor_v1**: AI model service using Scikit-learn
- **smv_secure-access-group**: AWS Security Group for access control
- **smv_cloud-insight**: Monitoring dashboard with CloudWatch and Grafana

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              smv_data-ai-node (EC2)                   │  │
│  │                                                        │  │
│  │  ┌──────────────────┐    ┌────────────────────────┐  │  │
│  │  │  smv_etl-pipeline│    │   smv_predictor_v1     │  │  │
│  │  │   (Docker)       │    │   (Docker)             │  │  │
│  │  │                  │    │                        │  │  │
│  │  │  S3 → Transform  │───▶│  Scikit-learn Model    │  │  │
│  │  │    → PostgreSQL  │    │  REST API (Port 8000)  │  │  │
│  │  └──────────────────┘    └────────────────────────┘  │  │
│  │                                                        │  │
│  │  ┌──────────────────┐    ┌────────────────────────┐  │  │
│  │  │   PostgreSQL     │    │  smv_cloud-insight     │  │  │
│  │  │   Database       │    │  (Grafana)             │  │  │
│  │  │                  │    │  (Port 3000)           │  │  │
│  │  └──────────────────┘    └────────────────────────┘  │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│         ▲                                                   │
│         │                                                   │
│  ┌──────┴──────────────┐                                   │
│  │ smv_secure-access-  │                                   │
│  │ group (Security)    │                                   │
│  └─────────────────────┘                                   │
│                                                              │
│  ┌──────────────┐      ┌─────────────────────────────┐    │
│  │  S3 Bucket   │      │  CloudWatch                  │    │
│  │  (Data)      │      │  (Logs & Metrics)            │    │
│  └──────────────┘      └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. ETL Pipeline (smv_etl-pipeline)

The ETL pipeline extracts data from S3, transforms it, and loads it into PostgreSQL.

**Features:**
- Automated data extraction from S3 buckets
- Data transformation and cleaning
- Batch loading into PostgreSQL
- Error handling and logging
- Configurable via environment variables

**Location:** `/etl-pipeline/`

### 2. AI Model Service (smv_predictor_v1)

Machine learning model service using Scikit-learn for predictions.

**Features:**
- Random Forest Classifier/Regressor
- REST API for predictions
- Model training pipeline
- Model versioning
- Health check endpoints

**Location:** `/ai-model/`

**API Endpoints:**
- `GET /health` - Health check
- `POST /predict` - Make predictions
- `GET /model/info` - Model information
- `POST /model/reload` - Reload model

### 3. Infrastructure (AWS)

Terraform configuration for AWS infrastructure.

**Components:**
- EC2 instance (smv_data-ai-node)
- Security Group (smv_secure-access-group)
- IAM roles and policies
- S3 bucket for data storage
- CloudWatch logs and dashboard

**Location:** `/infrastructure/`

### 4. Monitoring Dashboard (smv_cloud-insight)

Grafana dashboard integrated with CloudWatch for comprehensive monitoring.

**Metrics:**
- System performance (CPU, Memory, Disk, Network)
- ETL pipeline status
- AI model predictions count
- Model accuracy
- Application logs

**Location:** `/monitoring/`

## Prerequisites

### For Local Development:
- Docker and Docker Compose
- Python 3.9+
- AWS account with credentials

### For AWS Deployment:
- Terraform >= 1.0
- AWS CLI configured
- SSH key pair in AWS
- Appropriate AWS permissions

## Quick Start

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/G4thm/AWS-Scenerio-2.git
   cd AWS-Scenerio-2
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

3. **Build and start services:**
   ```bash
   ./scripts/deploy-containers.sh
   ```

4. **Check service health:**
   ```bash
   ./scripts/health-check.sh
   ```

5. **Access services:**
   - AI Model API: http://localhost:8000
   - Grafana Dashboard: http://localhost:3000 (admin/admin)
   - PostgreSQL: localhost:5432

### AWS Deployment

1. **Configure Terraform variables:**
   ```bash
   cd infrastructure
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your configuration
   ```

2. **Deploy infrastructure:**
   ```bash
   ./scripts/deploy-infrastructure.sh
   ```

3. **SSH to EC2 instance:**
   ```bash
   ssh -i your-key.pem ubuntu@<public-ip>
   ```

4. **Deploy containers on EC2:**
   ```bash
   # On EC2 instance
   ./scripts/deploy-containers.sh
   ```

## Configuration

### ETL Pipeline Configuration

Edit `etl-pipeline/.env.example`:

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=smv-data-bucket
S3_DATA_PREFIX=raw-data/
POSTGRES_HOST=localhost
POSTGRES_DB=smv_database
BATCH_SIZE=1000
```

### AI Model Configuration

Edit `ai-model/.env.example`:

```bash
POSTGRES_HOST=localhost
POSTGRES_DB=smv_database
MODEL_PATH=/app/models/smv_predictor_v1.pkl
MODEL_VERSION=v1
TEST_SIZE=0.2
SERVICE_PORT=8000
```

### Infrastructure Configuration

Edit `infrastructure/terraform.tfvars`:

```hcl
aws_region = "us-east-1"
project_name = "smv"
instance_type = "t3.large"
key_name = "your-key-name"
db_password = "secure-password"
```

## Usage

### Running ETL Pipeline

```bash
# Using Docker Compose
docker-compose run --rm etl_pipeline

# Manually
cd etl-pipeline
python etl_script.py
```

### Training AI Model

```bash
# Using Docker Compose
docker-compose --profile training run --rm ai_model_train

# Manually
cd ai-model
python train_model.py
```

### Making Predictions

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [1.0, 2.0, 3.0]
  }'
```

### Monitoring

Access Grafana dashboard at http://localhost:3000 or http://<ec2-public-ip>:3000

Default credentials: admin/admin

## Security

### Security Group Rules (smv_secure-access-group)

- **SSH (22)**: Restricted access for administration
- **PostgreSQL (5432)**: Internal network only
- **AI Model API (8000)**: Controlled external access
- **Grafana (3000)**: Controlled external access
- **CloudWatch Agent (9090)**: Internal network only

### Best Practices

1. Change default passwords in production
2. Use AWS Secrets Manager for sensitive data
3. Restrict security group CIDR blocks
4. Enable S3 bucket encryption
5. Regularly update dependencies
6. Monitor CloudWatch logs

## Monitoring and Logging

### CloudWatch

- EC2 metrics (CPU, Memory, Network, Disk)
- Application logs
- Custom metrics for ETL and AI model
- Automated dashboards

### Grafana

- Real-time system metrics
- ETL pipeline status
- Model prediction metrics
- Model accuracy tracking
- Custom alerts

## Troubleshooting

### ETL Pipeline Issues

```bash
# Check ETL logs
docker-compose logs etl_pipeline

# Verify S3 access
aws s3 ls s3://smv-data-bucket/

# Check database connection
docker-compose exec postgres psql -U smv_user -d smv_database
```

### AI Model Issues

```bash
# Check model service logs
docker-compose logs ai_model_service

# Verify model file exists
docker-compose exec ai_model_service ls -la /app/models/

# Check model health
curl http://localhost:8000/health
```

### Infrastructure Issues

```bash
# Check Terraform state
cd infrastructure
terraform show

# View AWS resources
aws ec2 describe-instances --filters "Name=tag:Name,Values=smv_data-ai-node"
```

## Maintenance

### Updating Dependencies

```bash
# Update Python packages
cd etl-pipeline
pip install -r requirements.txt --upgrade

cd ../ai-model
pip install -r requirements.txt --upgrade
```

### Backup and Recovery

```bash
# Backup PostgreSQL database
docker-compose exec postgres pg_dump -U smv_user smv_database > backup.sql

# Backup AI model
docker-compose cp ai_model_service:/app/models/smv_predictor_v1.pkl ./backup/
```

### Scaling

- Increase EC2 instance size in `infrastructure/variables.tf`
- Add more worker containers in `docker-compose.yml`
- Configure auto-scaling groups in Terraform

## Development

### Adding New Features

1. Create feature branch
2. Update relevant component
3. Test locally with Docker Compose
4. Update documentation
5. Submit pull request

### Testing

```bash
# Test ETL pipeline
cd etl-pipeline
python -m pytest tests/

# Test AI model
cd ai-model
python -m pytest tests/
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/G4thm/AWS-Scenerio-2/issues
- Documentation: https://github.com/G4thm/AWS-Scenerio-2/wiki

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.
