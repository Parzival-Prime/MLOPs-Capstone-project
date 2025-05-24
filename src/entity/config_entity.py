import os
from src.constants import *
from dataclasses import dataclass, field
from datetime import datetime
from src.utils import load_yaml
from src.constants import PARAMS_FILE_PATH

TIMESTAMP: str = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')

params = load_yaml(file_path=PARAMS_FILE_PATH)

@dataclass
class TrainingPipelineConfig:
    training_pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR)
    timestamp: str = TIMESTAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR, INGESTED_DATA_FILE_NAME)
    blob_data_path: str = os.path.join(DATA_BLOB_DIR, DATA_FILE_NAME)
    
    
@dataclass
class DataTransformationConfig:
    transformed_data_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR)
    train_data_path: str = os.path.join(transformed_data_dir, TRAIN_DATA_FILE)
    test_data_path: str = os.path.join(transformed_data_dir, TEST_DATA_FILE)
    test_size: float = params['data_transformation']['test_size']
    
@dataclass
class FeatureEngineeringConfig:
    feature_engineering_dir: str = os.path.join(training_pipeline_config.artifact_dir, FEATURE_ENGINEERING_DIR)
    vectorizer_file_path: str = os.path.join(MODELS_DIR, VECTORIZER_FILE_NAME)
    max_features: str = params['feature_engineering']['max_features']
    featured_train_data_file_path: str = os.path.join(feature_engineering_dir, FEATURED_TRAIN_FILE_NAME)
    featured_test_data_file_path: str = os.path.join(feature_engineering_dir, FEATURED_TEST_FILE_NAME)


@dataclass
class ModelTrainerConfig:
    model_params: dict = field(default_factory=lambda: params['model_params'])
    model_object_file_path: str = os.path.join(MODELS_DIR, MODEL_OBJECT_FILE_NAME)
    