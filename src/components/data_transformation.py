import os
import pickle

import numpy as np
from pandas import DataFrame, read_csv
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

nltk.download('stopwords')
nltk.download('wordnet')

from src.logger import logging
from src.exception import CustomException, handle_exception
from src.entity.config_entity import DataTransformationConfig, DataIngestionConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact

logger = logging.getLogger('Data Transformation')


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

with open('models/stopwords.pkl', 'wb') as file:
    pickle.dump(stop_words, file)

def preprocess_text(text):
    """Helper function to preprocess a single text string."""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", ' ', text)
    text = text.replace('؛', "")
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return ' '.join(words)

def apply_preprocessing(series):
    return series.apply(preprocess_text)

preprocess_pipeline = Pipeline([('preprocess', FunctionTransformer(apply_preprocessing, validate=False))])


class DataTransformation:
    """Class for Data Transformation."""
    
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_transformation_config: DataTransformationConfig=DataTransformationConfig()):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        
        
    @handle_exception
    def preprocess_dataframe(self, dataframe: DataFrame) -> DataFrame:
        """Preprocess a dataframe, like encoding tags"""
        try:
            logger.info('Preprocessing test...')
            
            dataframe = dataframe[dataframe['sentiment'].isin(['positive', 'negative'])]
            dataframe.loc[:, 'sentiment'] = dataframe['sentiment'].replace({'positive': 1, 'negative': 0})
            
            logger.info('Text Preprocessing Completed!')
            return dataframe
        except KeyError as e:
            logger.error('Missing column in the dataframe: %s', e)
            raise
        except Exception as e:
            logger.error('Unexpected error occured while preprocessing dataframe!')
            raise CustomException(e)
        
    
    @handle_exception
    def transform_dataframe(self, dataframe: DataFrame, col: str='review') -> DataFrame:
        """
        Transform a DataFrame by applying text preprocessing to a specific column.

        Args:
            dataframe (pd.DataFrame): The DataFrame to preprocess.
            col (str): The name of the column containing text.

        Returns:
            pd.DataFrame: The preprocessed DataFrame.
        """
        try:
            logger.info('Transforming text...')
                            
            dataframe[col] = preprocess_pipeline.transform(dataframe[col])
            
            dataframe = dataframe.dropna(subset=[col])
            
            logger.info('Text Transformation Completed!')
            return dataframe
        except Exception as e:
            logger.error('Error occured in transform_dataframe() method!')
            raise CustomException(e)
        
    
    @handle_exception
    def save_transformed_data(self, train_data: DataFrame, test_data: DataFrame):
        """This function takes raw data and uses to preprocess_dataframe() method to perform transformation and save it to artifact."""
        try:
            logger.info('Saving train_data and test_data files')
            os.makedirs(os.path.dirname(self.data_transformation_config.train_data_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.test_data_file_path), exist_ok=True)
            
            train_data.to_csv(self.data_transformation_config.train_data_file_path)
            test_data.to_csv(self.data_transformation_config.test_data_file_path)
            logger.info('Train and Test data files saved to artifact!')
            
        except Exception as e:
            logger.error('Error occured in load_transform_and_save() method.')
            raise CustomException(e)
        
        
    @handle_exception
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """Initiates data transformation."""
        
        try:
            logger.info('Inititated Data Transformation...')
            
            dataframe = read_csv(self.data_ingestion_artifact.raw_data_file_path)
            dataframe = self.preprocess_dataframe(dataframe)
            
            train_data, test_data = train_test_split(dataframe, test_size=self.data_transformation_config.test_size, random_state=42)
            train_data = self.transform_dataframe(train_data)
            test_data = self.transform_dataframe(test_data)
            
            self.save_transformed_data(train_data=train_data, test_data=test_data)
            
            data_transformation_artifact = DataTransformationArtifact(
                train_data_file_path=self.data_transformation_config.train_data_file_path,
                test_data_file_path=self.data_transformation_config.test_data_file_path
            )
            
            logger.info('Data Transformation Completed!')
            return data_transformation_artifact
        except Exception as e:
            logger.error('Unexpected error occured in initiate_data_transformation() method.')
            raise CustomException(e)
        
def main():
    """Main function"""
    data_ingestion_config = DataIngestionConfig()
    data_transformation = DataTransformation(data_ingestion_artifact=DataIngestionArtifact(raw_data_file_path=data_ingestion_config.raw_data_file_path))
    data_transformation.initiate_data_transformation()
    
if __name__=="__main__":
    main()