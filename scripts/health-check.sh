#!/bin/bash
set -e

echo "=========================================="
echo "SMV Service Health Check"
echo "=========================================="

# Check PostgreSQL
echo "Checking PostgreSQL..."
if docker-compose exec -T postgres pg_isready -U smv_user > /dev/null 2>&1; then
    echo "✓ PostgreSQL is healthy"
else
    echo "✗ PostgreSQL is not responding"
fi

# Check AI Model Service
echo "Checking AI Model Service..."
if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ AI Model Service is healthy"
    curl -s http://localhost:8000/health | python3 -m json.tool
else
    echo "✗ AI Model Service is not responding"
fi

# Check Grafana
echo "Checking Grafana..."
if curl -f -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✓ Grafana is healthy"
else
    echo "✗ Grafana is not responding"
fi

echo ""
echo "=========================================="
echo "Health check completed"
echo "=========================================="
