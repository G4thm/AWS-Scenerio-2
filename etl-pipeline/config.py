import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'smv-data-bucket')
S3_DATA_PREFIX = os.getenv('S3_DATA_PREFIX', 'raw-data/')

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'smv_database')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'smv_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'smv_password')

# ETL Configuration
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1000'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
