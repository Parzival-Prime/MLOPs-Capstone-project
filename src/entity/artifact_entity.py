from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    raw_data_file_path: str


@dataclass
class DataTransformationArtifact:
    train_data_path: str
    test_data_path: str
    
    
@dataclass
class FeatureEngineeringArtifact:
    featured_train_data_path: str
    featured_test_data_path: str
    vectorizer_file_path: str
    

@dataclass
class ModelTrainerArtifact:
    model_object_file_path: str