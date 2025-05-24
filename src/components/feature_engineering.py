import os
import yaml
import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from src.logger import logging
from src.constants import ROOT_DIR
from src.utils import load_csv, save_binary_file
from src.exception import handle_exception, CustomException
from src.entity.config_entity import FeatureEngineeringConfig, DataTransformationConfig
from src.entity.artifact_entity import FeatureEngineeringArtifact, DataTransformationArtifact

logger = logging.getLogger('Feature Engineering')


class FeatureEngineering:
    """This class is responsible for Feature Engineering in pipeline."""
    
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, feature_engineering_config: FeatureEngineeringConfig=FeatureEngineeringConfig()):

        self.data_transformation_artifact = data_transformation_artifact
        self.feature_engineering_config = feature_engineering_config
        
    
    @handle_exception
    def apply_bow(self, train_data: pd.DataFrame, test_data: pd.DataFrame, max_features: int) -> tuple:
        """Apply Count Vectorizer to the data."""
        try:
            logger.info('Applying Bag of Words to the data...')
            vectorizer = CountVectorizer(max_features=max_features)
            
            X_train = train_data['review'].values
            y_train = train_data['sentiment'].values
            X_test = test_data['review'].values
            y_test = test_data['sentiment'].values
            
            logger.debug('Transforming X_train and X_test with bag of words...')
            X_train_bow = vectorizer.fit_transform(X_train)
            X_test_bow = vectorizer.transform(X_test)
            logger.debug('Tranformation Successful!')
            
            logger.debug(f'Type of X_train_bow: {type(X_train_bow)}')
            logger.debug(f'Type of X_test_bow: {type(X_test_bow)}')
            
            train_df = pd.DataFrame(X_train_bow.toarray())
            train_df['label'] = y_train
            
            test_df = pd.DataFrame(X_test_bow.toarray())
            test_df['label'] = y_test
            logger.debug(f'X_train_bow and X_test_bow converted into {type(train_df)} and merged respective labels.')
        
            logger.info('Bag of words applied and Data Transformed.')
            
            logger.debug(f'Saving Vectorizer object to {os.path.relpath(path=self.feature_engineering_config.vectorizer_file_path, start=ROOT_DIR)}')
            
            os.makedirs(os.path.dirname(self.feature_engineering_config.vectorizer_file_path), exist_ok=True)
            
            save_binary_file(obj=vectorizer, file_path=self.feature_engineering_config.vectorizer_file_path)
            logger.debug(f'Vectorizer object saved to {os.path.relpath(start=ROOT_DIR, path=self.feature_engineering_config.vectorizer_file_path)}')
            
            return train_df, test_df
        except Exception as e:
            logger.error(f'Error during bag of words transformation: {e}')
            raise
    
    @handle_exception
    def save_data(self, dataframe: pd.DataFrame, file_path: str) -> None:
        """Save the dataframe to a csv file"""
        try:
            logger.info(f'Saving {os.path.basename(file_path)} to {os.path.relpath(path=file_path, start=ROOT_DIR)}')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            dataframe.to_csv(file_path, index=False)
            
            logger.info(f'File saved!')
        except Exception as e:
            logger.error(f'Unexpected error occured while saving data in feature engineering')
            raise
    
    
    @handle_exception
    def initiate_feature_engineering(self) -> FeatureEngineeringArtifact:
        """This method is responsible for initiating feature engineering."""
        try:
            logger.info('Initiated Feature Engineering Process...')
            train_data = load_csv(self.data_transformation_artifact.train_data_file_path)
            test_data = load_csv(self.data_transformation_artifact.test_data_file_path)
            
            train_df, test_df = self.apply_bow(train_data=train_data, test_data=test_data, max_features=self.feature_engineering_config.max_features)
            
            self.save_data(dataframe=train_df, file_path=self.feature_engineering_config.featured_train_data_file_path)
            self.save_data(dataframe=test_df, file_path=self.feature_engineering_config.featured_test_data_file_path)
            
            logger.info('Feature Engineering Completed!')
            
            feature_engineering_artifact = FeatureEngineeringArtifact(
                featured_train_data_file_path=self.feature_engineering_config.featured_train_data_file_path,
                featured_test_data_file_path=self.feature_engineering_config.featured_test_data_file_path,
                vectorizer_file_path=self.feature_engineering_config.vectorizer_file_path
            )
            logger.debug('Returned Feature Engineering Artifact.')
            
            return feature_engineering_artifact
        except Exception as e:
            logger.error(f'Failed to Complete Feature Engineering Process: {e}')
            raise
    
        
def main():
    """Main Function"""
    data_transformation_config = DataTransformationConfig()
    feature_engineering = FeatureEngineering(
        data_transformation_artifact=DataTransformationArtifact(
            train_data_file_path=data_transformation_config.train_data_file_path, 
            test_data_file_path=data_transformation_config.test_data_file_path
            ))
    feature_engineering.initiate_feature_engineering()
    
if __name__=='__main__':
    main()