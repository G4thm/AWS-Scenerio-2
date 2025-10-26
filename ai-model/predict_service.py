#!/usr/bin/env python3
"""
Prediction service for smv_predictor_v1 AI model
Provides REST API for model predictions
"""

import logging
import sys
from datetime import datetime
from flask import Flask, request, jsonify
import joblib
import numpy as np
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model storage
model_data = None


def load_model():
    """Load the trained model"""
    global model_data
    try:
        logger.info(f"Loading model from {config.MODEL_PATH}")
        model_data = joblib.load(config.MODEL_PATH)
        logger.info(f"Model loaded successfully - Version: {model_data.get('version', 'unknown')}")
        logger.info(f"Trained at: {model_data.get('trained_at', 'unknown')}")
        return True
    except FileNotFoundError:
        logger.error(f"Model file not found at {config.MODEL_PATH}")
        return False
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'smv_predictor_v1',
        'version': model_data.get('version', 'unknown') if model_data else 'no model loaded',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        if model_data is None:
            return jsonify({
                'error': 'Model not loaded'
            }), 503
        
        # Get input data
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({
                'error': 'Missing features in request'
            }), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Scale features
        features_scaled = model_data['scaler'].transform(features)
        
        # Make prediction
        prediction = model_data['model'].predict(features_scaled)
        
        # Get prediction probability if available (classification)
        response = {
            'prediction': prediction.tolist()[0],
            'model_version': model_data.get('version', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        if hasattr(model_data['model'], 'predict_proba'):
            proba = model_data['model'].predict_proba(features_scaled)
            response['probability'] = proba.tolist()[0]
        
        logger.info(f"Prediction made: {prediction}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Invalid input data: {e}")
        return jsonify({
            'error': 'Invalid input data format'
        }), 400
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return jsonify({
            'error': 'Prediction failed. Please check your input and try again.'
        }), 500


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    if model_data is None:
        return jsonify({
            'error': 'Model not loaded'
        }), 503
    
    return jsonify({
        'version': model_data.get('version', 'unknown'),
        'trained_at': model_data.get('trained_at', 'unknown'),
        'model_type': type(model_data['model']).__name__
    }), 200


@app.route('/model/reload', methods=['POST'])
def reload_model():
    """Reload the model"""
    if load_model():
        return jsonify({
            'status': 'success',
            'message': 'Model reloaded successfully'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to reload model'
        }), 500


def main():
    """Main entry point"""
    logger.info("Starting smv_predictor_v1 prediction service...")
    
    # Load model on startup
    if not load_model():
        logger.warning("Model not loaded - service starting without model")
        logger.warning("Train a model first or load an existing model")
    
    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=config.SERVICE_PORT,
        debug=False
    )


if __name__ == "__main__":
    main()
