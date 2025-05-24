from dataclasses import dataclass

from matplotlib import container

@dataclass
class DataIngestionArtifact:
    raw_data_file_path: str


@dataclass
class DataTransformationArtifact:
    train_data_file_path: str
    test_data_file_path: str
    
    
@dataclass
class FeatureEngineeringArtifact:
    featured_train_data_file_path: str
    featured_test_data_file_path: str
    vectorizer_file_path: str
    

@dataclass
class ModelTrainerArtifact:
    model_object_file_path: str
    

@dataclass
class ModelEvaluationArtifact:
    metrics_file_path: str
    experiment_info_file_path: str
    
@dataclass
class ModelPusherArtifact:
    model_blob_file_path: str
    container_name: str