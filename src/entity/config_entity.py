import os
from src.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')


@dataclass
class TrainingPipelineConfig:
    training_pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR)
    raw_data_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_RAW_DIR, DATA_FILE_NAME)
    blob_data_path: str = os.path.join(DATA_BLOB_DIR, DATA_FILE_NAME)
    
