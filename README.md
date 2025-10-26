# AWS Scenario 2: Cloud-Based Data Processing and AI Deployment

![Architecture](https://img.shields.io/badge/AWS-Cloud-orange?style=flat-square&logo=amazon-aws)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square&logo=docker)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=flat-square&logo=python)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?style=flat-square&logo=terraform)

A comprehensive cloud-based data processing and AI deployment infrastructure on AWS, featuring automated ETL pipelines, machine learning model services, and real-time monitoring.

## 🚀 Features

- **🔄 ETL Pipeline** (`smv_etl-pipeline`): Automated data extraction from S3, transformation, and loading into PostgreSQL
- **🤖 AI Model Service** (`smv_predictor_v1`): Scikit-learn-based ML model with REST API for predictions
- **☁️ AWS Infrastructure**: Fully automated deployment with Terraform
- **🔒 Security**: AWS Security Group (`smv_secure-access-group`) with restricted access rules
- **📊 Monitoring**: Integrated Grafana and CloudWatch dashboard (`smv_cloud-insight`)
- **🐳 Containerized**: All services run in Docker containers for easy deployment

## 📋 Quick Start

### Prerequisites
- Docker and Docker Compose
- AWS account with credentials
- (Optional) Terraform for AWS deployment

### Local Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/G4thm/AWS-Scenerio-2.git
cd AWS-Scenerio-2

# 2. Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# 3. Deploy services
./scripts/deploy-containers.sh

# 4. Check health
./scripts/health-check.sh
```

### Access Services

- **AI Model API**: http://localhost:8000
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **PostgreSQL**: localhost:5432

## 📦 Components

### 1. EC2 Instance (smv_data-ai-node)
Main compute instance hosting all data processing and AI services.

### 2. ETL Pipeline (smv_etl-pipeline)
Docker container that:
- Extracts data from AWS S3
- Transforms and cleans data
- Loads into PostgreSQL database

### 3. AI Model (smv_predictor_v1)
Machine learning service with:
- Scikit-learn Random Forest model
- REST API for predictions
- Automated training pipeline
- Model versioning

### 4. Security Group (smv_secure-access-group)
AWS Security Group controlling:
- SSH access (port 22)
- API access (port 8000)
- Database access (port 5432)
- Dashboard access (port 3000)

### 5. Monitoring (smv_cloud-insight)
Comprehensive monitoring with:
- Grafana dashboards
- CloudWatch metrics
- System performance tracking
- Model accuracy monitoring
- ETL pipeline status

## 🏗️ Architecture

```
AWS Cloud
├── EC2 Instance (smv_data-ai-node)
│   ├── smv_etl-pipeline (Docker)
│   ├── smv_predictor_v1 (Docker)
│   ├── PostgreSQL Database
│   └── smv_cloud-insight (Grafana)
├── S3 Bucket (Data Storage)
├── CloudWatch (Logs & Metrics)
└── Security Group (smv_secure-access-group)
```

## 📚 Documentation

- **[Full Documentation](docs/README.md)** - Complete guide with architecture details
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[API Documentation](docs/API.md)** - REST API endpoints and examples

## 🔧 Configuration

### ETL Pipeline
Configure in `etl-pipeline/.env.example`:
- AWS credentials and S3 bucket
- PostgreSQL connection
- Batch size and logging

### AI Model
Configure in `ai-model/.env.example`:
- Database connection
- Model parameters
- Service port and version

### Infrastructure
Configure in `infrastructure/terraform.tfvars.example`:
- AWS region and instance type
- Security group rules
- S3 bucket settings

## 🚀 Deployment

### Local Development
```bash
./scripts/deploy-containers.sh
```

### AWS Production
```bash
./scripts/deploy-infrastructure.sh
```

## 📊 Usage Examples

### Make a Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.5, 2.3, 3.7]}'
```

### Run ETL Pipeline
```bash
docker-compose run --rm etl_pipeline
```

### Train Model
```bash
docker-compose --profile training run --rm ai_model_train
```

### View Logs
```bash
docker-compose logs -f ai_model_service
```

## 🔍 Monitoring

Access Grafana at http://localhost:3000 to view:
- Real-time system metrics
- ETL pipeline status
- Model prediction metrics
- Resource utilization
- Custom alerts

## 🛠️ Troubleshooting

Run the health check script:
```bash
./scripts/health-check.sh
```

View service logs:
```bash
docker-compose logs [service-name]
```

See [Documentation](docs/README.md#troubleshooting) for detailed troubleshooting guide.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/G4thm/AWS-Scenerio-2/issues)
- **API Reference**: [docs/API.md](docs/API.md)

---

**Built with ❤️ using AWS, Docker, Python, and Terraform**
