import os
from datetime import datetime
from from_root import from_root
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(from_root())

env_file_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(env_file_path)

# Logging
LOG_DIR='logs'
LOG_FILENAME = f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.log"
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3
FILE_HANLDER_ENCODING='utf-8'



# Model and files
MODEL_DIR = os.path.join(ROOT_DIR, 'models')
MODEL_NAME = 'model.pkl'
MODEL_BLOB_NAME = 'model.pkl'
MODEL_BLOB_DIR = 'models'
DATA_BLOB_DIR = 'data'
DATA_FILE_NAME = 'data.csv' # IMDB.csv

# Azure
BLOB_CONTAINER = 'capstoneprojcunt'
BLOB_STORAGE_REGION='eastasia'
BLOB_STORAGE_INSTANCE_NAME=os.getenv('BLOB_STORAGE_INSTANCE_NAME')
AZURE_TENANT_ID=os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.getenv('AZURE_CLIENT_SECRET')
AZURE_STORAGE_ACCOUNT_URL=os.getenv('AZURE_STORAGE_ACCOUNT_URL')
SERVICE_PRINCIPLE_ID=os.getenv('SERVICE_PRINCIPLE_ID')

# pipeline
PIPELINE_NAME: str = ''
ARTIFACT_DIR: str = 'artifact'
TEST_SIZE: float = 0.2

# Data Ingestion
DATA_INGESTION_DIR: str = 'ingested_data'
DATA_INGESTION_RAW_DIR: str = 'raw_data'

# Data Transformation
DATA_TRANSFORMATION_DIR: str = 'transformed_data'
TRAIN_DATA_FILE: str = 'train.csv'
TEST_DATA_FILE: str = 'test.csv'

# Feature Engineering
FEATURE_ENGINEERING_DIR: str = 'feature'
VECTORIZER_FILE_NAME: str = 'vectorizer.pkl'
MAX_FEATURES: int = 20
FEATURED_DATA_DIR: str = 'data'
FEATURED_TRAIN_FILE_NAME: str = 'train.csv'
FEATURED_TEST_FILE_NAME: str = 'test.csv' 