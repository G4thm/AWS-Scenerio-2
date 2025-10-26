import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'smv_database')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'smv_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'smv_password')

# Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', '/app/models/smv_predictor_v1.pkl')
MODEL_VERSION = os.getenv('MODEL_VERSION', 'v1')

# Training Configuration
TEST_SIZE = float(os.getenv('TEST_SIZE', '0.2'))
RANDOM_STATE = int(os.getenv('RANDOM_STATE', '42'))

# Service Configuration
SERVICE_PORT = int(os.getenv('SERVICE_PORT', '8000'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
