#!/usr/bin/env python3
"""
ETL Pipeline for smv_etl-pipeline
Extracts data from S3, transforms it, and loads it into PostgreSQL
"""

import logging
import sys
from datetime import datetime
import boto3
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from io import StringIO
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL Pipeline class for data processing"""
    
    def __init__(self):
        self.s3_client = None
        self.db_connection = None
        
    def connect_s3(self):
        """Connect to AWS S3"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )
            logger.info("Successfully connected to S3")
        except Exception as e:
            logger.error(f"Failed to connect to S3: {e}")
            raise
    
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
    
    def extract_from_s3(self, bucket_name, prefix):
        """Extract data files from S3 bucket"""
        try:
            logger.info(f"Extracting data from S3 bucket: {bucket_name}/{prefix}")
            response = self.s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix
            )
            
            data_files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    if obj['Key'].endswith('.csv'):
                        data_files.append(obj['Key'])
            
            logger.info(f"Found {len(data_files)} CSV files to process")
            return data_files
        except Exception as e:
            logger.error(f"Failed to extract data from S3: {e}")
            raise
    
    def transform_data(self, data):
        """Transform the extracted data"""
        try:
            logger.info("Transforming data...")
            
            # Basic data cleaning
            data = data.dropna()
            
            # Add timestamp for tracking
            data['processed_at'] = datetime.now()
            
            # Add any additional transformations here
            logger.info(f"Transformed {len(data)} records")
            return data
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            raise
    
    def load_to_database(self, data, table_name='processed_data'):
        """Load transformed data into PostgreSQL"""
        try:
            logger.info(f"Loading data into table: {table_name}")
            
            cursor = self.db_connection.cursor()
            
            # Create table if it doesn't exist
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                processed_at TIMESTAMP,
                data JSONB
            );
            """
            cursor.execute(create_table_query)
            
            # Insert data in batches
            insert_query = f"INSERT INTO {table_name} (processed_at, data) VALUES (%s, %s)"
            
            records = [
                (row['processed_at'], row.to_json())
                for _, row in data.iterrows()
            ]
            
            execute_batch(cursor, insert_query, records, page_size=config.BATCH_SIZE)
            
            self.db_connection.commit()
            cursor.close()
            
            logger.info(f"Successfully loaded {len(data)} records into {table_name}")
        except Exception as e:
            logger.error(f"Failed to load data into database: {e}")
            if self.db_connection:
                self.db_connection.rollback()
            raise
    
    def run_pipeline(self):
        """Execute the complete ETL pipeline"""
        try:
            logger.info("Starting ETL pipeline...")
            start_time = datetime.now()
            
            # Connect to services
            self.connect_s3()
            self.connect_database()
            
            # Extract
            data_files = self.extract_from_s3(config.S3_BUCKET_NAME, config.S3_DATA_PREFIX)
            
            for file_key in data_files:
                logger.info(f"Processing file: {file_key}")
                
                # Download file from S3
                obj = self.s3_client.get_object(Bucket=config.S3_BUCKET_NAME, Key=file_key)
                data = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
                
                # Transform
                transformed_data = self.transform_data(data)
                
                # Load
                self.load_to_database(transformed_data)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"ETL pipeline completed successfully in {duration:.2f} seconds")
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise
        finally:
            if self.db_connection:
                self.db_connection.close()


def main():
    """Main entry point"""
    try:
        pipeline = ETLPipeline()
        pipeline.run_pipeline()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
