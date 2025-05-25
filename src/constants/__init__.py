import os
from datetime import datetime
from from_root import from_root
from pathlib import Path
import logging

ROOT_DIR = Path(from_root())

if os.getenv('ENV') != 'Production':
    from dotenv import load_dotenv
    env_file_path = os.path.join(ROOT_DIR, '.env')
    load_dotenv(env_file_path)

# Logging
LOG_DIR='logs'
LOG_FILENAME = f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.log"
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3
FILE_HANLDER_ENCODING='utf-8'
LOG_LEVEL= logging.DEBUG if os.getenv('ENV')=='dev' else logging.INFO



# Miscellaneous
DATA_FILE_NAME: str = 'data.csv' # IMDB.csv
PARAMS_FILE_PATH: str = 'params.yaml'


# Azure
BLOB_CONTAINER = 'capstoneprojcunt'
BLOB_STORAGE_REGION='eastasia'
AZURE_TENANT_ID=os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.getenv('AZURE_CLIENT_SECRET')
AZURE_STORAGE_ACCOUNT_URL=os.getenv('AZURE_STORAGE_ACCOUNT_URL')
SERVICE_PRINCIPLE_ID=os.getenv('SERVICE_PRINCIPLE_ID')
DATA_BLOB_DIR: str = 'data'
DVC_REPO_FOLDER: str = 'dvcstore'


# DagsHub and MLFlow
DAGSHUB_URL: str = "https://dagshub.com"
DAGSHUB_REPO_OWNER: str = 'Parzival-Prime'
DAGSHUB_REPO_NAME: str = 'MLOPs-Capstone-project'

# pipeline
PIPELINE_NAME: str = ''
ARTIFACT_DIR: str = 'artifact'

# Data Ingestion
DATA_INGESTION_DIR: str = 'ingested_data'
INGESTED_DATA_FILE_NAME: str = 'data.csv'

# Data Transformation
DATA_TRANSFORMATION_DIR: str = 'transformed_data'
TRAIN_DATA_FILE: str = 'train.csv'
TEST_DATA_FILE: str = 'test.csv'

# Feature Engineering
FEATURE_ENGINEERING_DIR: str = 'feature'
VECTORIZER_FILE_NAME: str = 'vectorizer.pkl'
MAX_FEATURES: int = 20
FEATURED_TRAIN_FILE_NAME: str = 'train.csv'
FEATURED_TEST_FILE_NAME: str = 'test.csv' 

# Model Training
MODEL_OBJECT_FILE_NAME: str = 'model.pkl'

# Model Evaluation
REPORTS_DIR: str = 'reports'
METRICS_FILE_NAME: str = 'metrics.json'
EXPERIMENT_INFO_FILE_NAME: str = 'experiment_info.json'
MODEL_STAGE: str = 'Staging'
MODEL_NAME: str = 'imdb_sentiment_model2'
MODELS_DIR: str = 'models'

# Model Pusher
MODEL_BLOB_NAME: str = 'model.pkl'
MODEL_BLOB_DIR: str = 'models'