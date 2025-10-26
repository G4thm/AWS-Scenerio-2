# API Documentation

## AI Model Prediction Service (smv_predictor_v1)

Base URL: `http://localhost:8000` (local) or `http://<ec2-ip>:8000` (production)

### Endpoints

#### 1. Health Check

Check if the service is running and healthy.

**Request:**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "smv_predictor_v1",
  "version": "v1",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is not ready

**Example:**
```bash
curl http://localhost:8000/health
```

---

#### 2. Make Prediction

Submit features for prediction by the AI model.

**Request:**
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "features": [1.5, 2.3, 3.7]
}
```

**Response (Classification):**
```json
{
  "prediction": 1,
  "probability": [0.23, 0.77],
  "model_version": "v1",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Response (Regression):**
```json
{
  "prediction": 42.5,
  "model_version": "v1",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Status Codes:**
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Prediction failed
- `503 Service Unavailable` - Model not loaded

**Example:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [1.5, 2.3, 3.7]
  }'
```

**Python Example:**
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "features": [1.5, 2.3, 3.7]
}

response = requests.post(url, json=data)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Model version: {result['model_version']}")
```

---

#### 3. Model Information

Get information about the currently loaded model.

**Request:**
```http
GET /model/info
```

**Response:**
```json
{
  "version": "v1",
  "trained_at": "2024-01-15T08:00:00.000Z",
  "model_type": "RandomForestClassifier"
}
```

**Status Codes:**
- `200 OK` - Model information retrieved
- `503 Service Unavailable` - Model not loaded

**Example:**
```bash
curl http://localhost:8000/model/info
```

---

#### 4. Reload Model

Reload the model from disk (useful after retraining).

**Request:**
```http
POST /model/reload
```

**Response:**
```json
{
  "status": "success",
  "message": "Model reloaded successfully"
}
```

**Status Codes:**
- `200 OK` - Model reloaded successfully
- `500 Internal Server Error` - Failed to reload model

**Example:**
```bash
curl -X POST http://localhost:8000/model/reload
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Description of the error"
}
```

### Common Errors

#### Missing Features
```json
{
  "error": "Missing features in request"
}
```

#### Model Not Loaded
```json
{
  "error": "Model not loaded"
}
```

#### Internal Error
```json
{
  "error": "Prediction failed: <error details>"
}
```

---

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider implementing rate limiting based on your requirements.

---

## Authentication

Currently, the API does not require authentication. For production use, implement API key authentication or OAuth2.

**Future Implementation Example:**
```bash
curl http://localhost:8000/predict \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"features": [1.5, 2.3, 3.7]}'
```

---

## Batch Predictions

For batch predictions, make multiple individual requests or implement a batch endpoint.

**Example Script:**
```python
import requests
import concurrent.futures

def make_prediction(features):
    url = "http://localhost:8000/predict"
    response = requests.post(url, json={"features": features})
    return response.json()

# Batch data
batch_features = [
    [1.5, 2.3, 3.7],
    [2.1, 3.4, 4.2],
    [0.8, 1.9, 2.5]
]

# Make parallel requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(make_prediction, batch_features))

for i, result in enumerate(results):
    print(f"Prediction {i+1}: {result['prediction']}")
```

---

## Monitoring

### Metrics

The service logs the following information:
- Request timestamps
- Prediction inputs and outputs
- Model version used
- Error messages

### Health Monitoring

Set up automated health checks:

```bash
#!/bin/bash
# health-monitor.sh

while true; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "$(date): Service is healthy"
    else
        echo "$(date): Service is DOWN - alerting..."
        # Send alert here
    fi
    sleep 60
done
```

---

## WebSocket Support

Currently not implemented. For real-time predictions, make periodic HTTP requests or implement WebSocket support.

---

## CORS

By default, CORS is not configured. To enable CORS for web applications, add CORS middleware to the Flask app.

**Example Configuration:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
```

---

## Performance

### Response Times
- Health check: < 50ms
- Prediction: 50-200ms (depends on model complexity)
- Model info: < 50ms
- Model reload: 1-5s (depends on model size)

### Optimization Tips
1. Use model caching
2. Implement request batching
3. Use connection pooling
4. Deploy multiple service instances
5. Use load balancer for distribution

---

## Versioning

The API version is included in the response:
- Current version: v1
- Version is embedded in model metadata
- Breaking changes will increment major version

---

## Support

For API issues or questions:
- Check service logs: `docker-compose logs ai_model_service`
- Verify model is loaded: `GET /model/info`
- Check health status: `GET /health`
- Consult documentation: [README.md](./README.md)
