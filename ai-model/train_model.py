#!/usr/bin/env python3
"""
Training script for smv_predictor_v1 AI model
Uses Scikit-learn for machine learning
"""

import logging
import sys
from datetime import datetime
import numpy as np
import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import joblib
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """AI Model Training class using Scikit-learn"""
    
    def __init__(self):
        self.db_connection = None
        self.model = None
        self.scaler = StandardScaler()
        
    def connect_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.db_connection = psycopg2.connect(
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                dbname=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD
            )
            logger.info("Successfully connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def load_training_data(self):
        """Load training data from PostgreSQL"""
        try:
            logger.info("Loading training data from database...")
            
            query = """
            SELECT * FROM processed_data 
            ORDER BY processed_at DESC 
            LIMIT 10000;
            """
            
            data = pd.read_sql(query, self.db_connection)
            logger.info(f"Loaded {len(data)} records for training")
            
            return data
        except Exception as e:
            logger.error(f"Failed to load training data: {e}")
            raise
    
    def preprocess_data(self, data):
        """Preprocess data for training"""
        try:
            logger.info("Preprocessing data...")
            
            # This is a placeholder - adjust based on actual data structure
            # For demonstration, assuming numeric features
            feature_columns = [col for col in data.columns 
                             if col not in ['id', 'processed_at', 'data']]
            
            if len(feature_columns) == 0:
                logger.warning("No feature columns found, creating synthetic features for demo")
                # Create synthetic features for demonstration
                np.random.seed(config.RANDOM_STATE)
                n_samples = len(data)
                data['feature_1'] = np.random.randn(n_samples)
                data['feature_2'] = np.random.randn(n_samples)
                data['feature_3'] = np.random.randn(n_samples)
                data['target'] = (data['feature_1'] + data['feature_2'] > 0).astype(int)
                
                feature_columns = ['feature_1', 'feature_2', 'feature_3']
                target_column = 'target'
            else:
                # Use actual data
                target_column = feature_columns[-1]
                feature_columns = feature_columns[:-1]
            
            X = data[feature_columns]
            y = data[target_column]
            
            logger.info(f"Features: {feature_columns}")
            logger.info(f"Target: {target_column}")
            
            return X, y, feature_columns, target_column
        except Exception as e:
            logger.error(f"Failed to preprocess data: {e}")
            raise
    
    def train_model(self, X_train, y_train):
        """Train the machine learning model"""
        try:
            logger.info("Training model...")
            
            # Determine if classification or regression
            if len(np.unique(y_train)) < 20:
                logger.info("Using Random Forest Classifier")
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=config.RANDOM_STATE,
                    n_jobs=-1
                )
            else:
                logger.info("Using Random Forest Regressor")
                self.model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=config.RANDOM_STATE,
                    n_jobs=-1
                )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            logger.info("Model training completed")
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            raise
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model"""
        try:
            logger.info("Evaluating model...")
            
            # Scale test features
            X_test_scaled = self.scaler.transform(X_test)
            
            # Make predictions
            y_pred = self.model.predict(X_test_scaled)
            
            # Calculate metrics
            if hasattr(self.model, 'predict_proba'):
                # Classification metrics
                accuracy = accuracy_score(y_test, y_pred)
                logger.info(f"Model Accuracy: {accuracy:.4f}")
            else:
                # Regression metrics
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                logger.info(f"Model MSE: {mse:.4f}")
                logger.info(f"Model R2 Score: {r2:.4f}")
            
        except Exception as e:
            logger.error(f"Failed to evaluate model: {e}")
            raise
    
    def save_model(self):
        """Save the trained model to disk"""
        try:
            logger.info(f"Saving model to {config.MODEL_PATH}")
            
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'version': config.MODEL_VERSION,
                'trained_at': datetime.now().isoformat()
            }
            
            joblib.dump(model_data, config.MODEL_PATH)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            raise
    
    def run_training_pipeline(self):
        """Execute the complete training pipeline"""
        try:
            logger.info("Starting model training pipeline...")
            start_time = datetime.now()
            
            # Connect to database
            self.connect_database()
            
            # Load data
            data = self.load_training_data()
            
            # Preprocess
            X, y, feature_cols, target_col = self.preprocess_data(data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=config.TEST_SIZE, 
                random_state=config.RANDOM_STATE
            )
            
            logger.info(f"Training set size: {len(X_train)}")
            logger.info(f"Test set size: {len(X_test)}")
            
            # Train
            self.train_model(X_train, y_train)
            
            # Evaluate
            self.evaluate_model(X_test, y_test)
            
            # Save
            self.save_model()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"Training pipeline completed successfully in {duration:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {e}")
            raise
        finally:
            if self.db_connection:
                self.db_connection.close()


def main():
    """Main entry point"""
    try:
        trainer = ModelTrainer()
        trainer.run_training_pipeline()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Training execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
