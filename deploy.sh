#!/bin/bash
echo "Deploying SMV Integration Stack..."

sudo apt update -y
sudo apt install -y docker docker-compose

cd /home/ubuntu/smv_integration
sudo docker-compose up -d --build

echo "All services are up and running!"
