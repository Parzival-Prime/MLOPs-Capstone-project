from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    raw_data_file_path: str

class DataValidationArtifact:
    validation_status: str
    message: str
    validation_report_file_path: str
    
# class DataTransformationArtifact:
    