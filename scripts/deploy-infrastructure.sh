#!/bin/bash
set -e

echo "=========================================="
echo "SMV Infrastructure Deployment Script"
echo "=========================================="

# Check prerequisites
command -v terraform >/dev/null 2>&1 || { echo "Error: terraform is required but not installed."; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "Error: aws CLI is required but not installed."; exit 1; }

# Navigate to infrastructure directory
cd "$(dirname "$0")/../infrastructure"

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "Error: terraform.tfvars not found. Please copy terraform.tfvars.example and configure it."
    exit 1
fi

echo "Initializing Terraform..."
terraform init

echo "Validating Terraform configuration..."
terraform validate

echo "Planning infrastructure deployment..."
terraform plan -out=tfplan

echo ""
read -p "Do you want to apply this plan? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo "Applying Terraform plan..."
    terraform apply tfplan
    
    echo ""
    echo "=========================================="
    echo "Infrastructure deployed successfully!"
    echo "=========================================="
    
    echo ""
    echo "Retrieving outputs..."
    terraform output
    
    echo ""
    echo "Next steps:"
    echo "1. SSH into the EC2 instance using the public IP"
    echo "2. Deploy application containers using deploy-containers.sh"
    echo "3. Access Grafana dashboard at http://<public-ip>:3000"
else
    echo "Deployment cancelled."
    rm -f tfplan
fi
