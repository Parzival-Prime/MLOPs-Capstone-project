import os
from datetime import datetime
from from_root import from_root
from dotenv import load_env #type: ignore
from pathlib import Path

ROOT_DIR = Path(from_root())

env_file_path = os.path.join(ROOT_DIR, '.env')
load_env(env_file_path)

#Logging
LOG_DIR='logs'
LOG_FILENAME = f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.log"
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3


#Azure
BLOB_STORAGE_REGION='eastasia'
BLOB_STORAGE_INSTANCE_NAME=os.getenv('BLOB_STORAGE_INSTANCE_NAME')
AZURE_TENANT_ID=os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.getenv('AZURE_CLIENT_SECRET')
AZURE_STORAGE_ACCOUNT_URL=os.getenv('AZURE_STORAGE_ACCOUNT_URL')
SERVICE_PRINCIPLE_ID=os.getenv('SERVICE_PRINCIPLE_ID')
