import os

from src.logger import logging
from src.exception import handle_exception, CustomException

from pandas import DataFrame, read_csv

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging
from src.exception import CustomException, handle_exception
from src.cloud_storage.azure_storage import AzureBlobStorage
from src.constants import BLOB_CONTAINER

logger = logging.getLogger('Data Ingestion')


class DataIngestion:
    """Class for Data Ingestion."""
    
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    @handle_exception
    def export_data_into_artifact(self):
        """This function imports data from cloud storage."""
        
        try:
            blob_storage_client = AzureBlobStorage()
            logger.info('Downloading data from Blob Storage...')
            
            blob_storage_client.download_file(
                file_blob_path=self.data_ingestion_config.blob_data_path,
                file_save_path=self.data_ingestion_config.raw_data_path,
                container_name=BLOB_CONTAINER
            )
            logger.info('Data downloaded!')
            
        except Exception as e:
            logger.error('Some Error occured in export_data_into_artifact()')
            raise CustomException(e)
        
        
    def initiate_data_ingestion(self):
        """Method to initiate data Ingestion."""
        try:
            logger.info('Data Ingestion Initiated...')
            self.export_data_into_artifact()
            
            data_ingestion_artifact = DataIngestionArtifact(raw_data_file_path=self.data_ingestion_config.raw_data_path)
            logger.info('Data Ingestion Completed!')
            
            return data_ingestion_artifact
        except Exception as e:
            logger.error('Some Error occured in Data Ingestion!')
            raise CustomException(e)