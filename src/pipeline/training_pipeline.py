from src.logger import logging
from src.exception import CustomException, handle_exception

from src.components.data_ingestion import DataIngestion 
from src.components.data_transformation import DataTransformation
from src.components.feature_engineering import FeatureEngineering
from src.components.model_training import ModelTrainer

from src.entity.config_entity import (DataIngestionConfig,
                                      DataTransformationConfig,
                                      FeatureEngineeringConfig,
                                      ModelTrainerConfig)

from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataTransformationArtifact,
                                        FeatureEngineeringArtifact,
                                        ModelTrainerArtifact)
 
logger = logging.getLogger('Training Pipeline')


class TrainingPipeline:
    
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.feature_engineering_config = FeatureEngineeringConfig()
        self.model_trainer_config = ModelTrainerConfig()
    
    
    @handle_exception    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e)
    
    @handle_exception
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config
                )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            return data_transformation_artifact
        except Exception as e:
            logger.error('Unexpected error occured in start_data_transformation() method!')
            raise CustomException(e)
    
    @handle_exception
    def start_feature_engineering(self, data_transformation_artifact: DataTransformationArtifact) -> FeatureEngineeringArtifact:
        """This method of TrainPipeline class is responsible for starting feature engineering component."""
        try:
            feature_engineering = FeatureEngineering(
                data_transformation_artifact=data_transformation_artifact,
                feature_engineering_config=self.feature_engineering_config
            )
            
            feature_engineering_artifact = feature_engineering.initiate_feature_engineering()
            
            return feature_engineering_artifact
        except Exception as e:
            logger.error('Unexpected error occured in start_feature_engineering() method1')
            raise CustomException(e)
        
    
    @handle_exception
    def start_model_training(self, feature_engineering_artifact: FeatureEngineeringArtifact) -> ModelTrainerArtifact:
        """This method of TrainPipeline class is responsible for starting Model Training component"""
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, feature_engineering_artifact=feature_engineering_artifact)
            
            model_training_artifact = model_trainer.initiate_model_training()
            
            return model_training_artifact
        except Exception as e:
            logger.error(f'An Unexpected error occured in start_model_training() method: {e}')
            raise CustomException(e)
    
    @handle_exception
    def initiate_training_pipeline(self):
        """This method is responsible for initiating training pipeline"""
        try:
            logger.info('Initiated Training Pipeline...')
            
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            
            feature_engineering_artifact = self.start_feature_engineering(data_transformation_artifact=data_transformation_artifact)
            
            model_training_artifact = self.start_model_training(feature_engineering_artifact=feature_engineering_artifact)
            
            logger.info('🎉🎉🎉Training Pipeline Completed! 🎋🌿')
        except Exception as e:
            logger.error('Unexpected error occured in initiate_training_pipeline() method!')
            raise CustomException(e)