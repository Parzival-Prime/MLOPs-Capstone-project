import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.logger import logging
from src.exception import handle_exception, CustomException
from src.utils import load_csv, load_yaml, save_binary_file
from src.entity.config_entity import ModelTrainerConfig, FeatureEngineeringConfig
from src.entity.artifact_entity import ModelTrainerArtifact, FeatureEngineeringArtifact

logger = logging.getLogger('Model Trainer')


class ModelTrainer:
    
    def __init__(self, 
                 feature_engineering_artifact: FeatureEngineeringArtifact, 
                 model_trainer_config: ModelTrainerConfig=ModelTrainerConfig()
                 ):
        
        self.feature_engineering_artifact = feature_engineering_artifact
        self.model_trainer_config = model_trainer_config
        
        
    def build_and_train_model(self, X_train: np.array, y_train: np.array, params: str) -> tuple[object, object]:
        """This function trains a Logistic Regression Model with specified parameters"""
        try:
            logger.debug('Loading Model Parameters file...')
            model = LogisticRegression(C=params['C'], solver=params['solver'], penalty=params['penalty'])
            
            logger.debug(f"Type of X_train: {type(X_train)}")
            logger.debug(f"Type of y_train: {type(y_train)}")
            
            logger.info('Training Model...')
            model.fit(X_train, y_train)
            logger.info('Model Trained!')
            
            return model
        except Exception as e:
            logger.error(f'Unexpected error occured in build_model_and_train_model() method: {e}')
            raise
        
    def initiate_model_training(self) -> ModelTrainerArtifact:
        """Initiates Model Training."""
        try:
            logger.debug('Loading Training Data...')
            train = load_csv(file_path=self.feature_engineering_artifact.featured_train_data_file_path)
            X_train, y_train = train.iloc[:, :-1].values, train.iloc[:, -1].values
            
            model = self.build_and_train_model(X_train=X_train, y_train=y_train, params=self.model_trainer_config.model_params)
            
            logger.debug('Saving Model Object...')
            save_binary_file(obj=model, file_path=self.model_trainer_config.model_object_file_path)
            
            model_trainer_artifact = ModelTrainerArtifact(model_object_file_path=self.model_trainer_config.model_object_file_path)
            
            return model_trainer_artifact
        except Exception as e:
            logger.error(f'An Unexpected error occured in initiate_model_training() method: {e}')
            raise
        

def main():
    """Main Function"""
    
    feature_engineering_config = FeatureEngineeringConfig()
    
    model_trainer = ModelTrainer(
        feature_engineering_artifact=FeatureEngineeringArtifact(
            featured_train_data_file_path=feature_engineering_config.featured_train_data_file_path, featured_test_data_file_path=feature_engineering_config.featured_test_data_file_path, vectorizer_file_path=feature_engineering_config.vectorizer_file_path
            )
        )
    
    model_trainer.initiate_model_training()
    
if __name__=='__main__':
    main()
    