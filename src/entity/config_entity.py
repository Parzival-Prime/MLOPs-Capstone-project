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
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR)
    raw_data_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_RAW_DIR, DATA_FILE_NAME)
    blob_data_path: str = os.path.join(DATA_BLOB_DIR, DATA_FILE_NAME)
    
@dataclass
class DataTransformationConfig:
    transformed_data_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR)
    train_data_path: str = os.path.join(transformed_data_dir, TRAIN_DATA_FILE)
    test_data_path: str = os.path.join(transformed_data_dir, TEST_DATA_FILE)
    test_size: float = TEST_SIZE
    
@dataclass
class FeatureEngineeringConfig:
    feature_engineering_dir: str = os.path.join(training_pipeline_config.artifact_dir, FEATURE_ENGINEERING_DIR)
    vectorizer_file_path: str = os.path.join(feature_engineering_dir, VECTORIZER_FILE_NAME)
    max_features: str = MAX_FEATURES
    featured_train_data_file_path: str = os.path.join(feature_engineering_dir, FEATURED_DATA_DIR, FEATURED_TRAIN_FILE_NAME)
    featured_test_data_file_path: str = os.path.join(feature_engineering_dir, FEATURED_DATA_DIR, FEATURED_TEST_FILE_NAME)
