import os
import pickle
import yaml

import pandas as pd

from src.logger import logging
from src.constants import ROOT_DIR

logger = logging.getLogger('Utils')


def save_binary_file(obj: object, file_path: str):
    """Saves the binary file to specified directory."""
    try:
        logger.debug(f'Saving binary file {os.path.basename(file_path)} to {os.path.dirname(file_path)}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file=file_path, mode='wb') as file:
            pickle.dump(obj=obj, file=file)
        logger.debug('File saved Successfully!')
    except pickle.PickleError as e:
        logger.error(f'A PickleError occured! : {e}')
        raise
    except Exception as e:
        logger.error(f'An Unexpected error occcured while saving binary file: {e}')
        

    
def load_yaml(file_path: str) -> yaml.YAMLObject: 
    """Loads a yaml file."""
    try:
        logger.debug(f'Loading YAML file: {os.path.relpath(path=file_path, start=ROOT_DIR)}')
        with open(file=file_path, mode='r') as file:
            params = yaml.safe_load(file)
        logger.debug('File Successfully loaded!')
        return params
    except yaml.YAMLError as e:
        logger.error(f'A YAMLError occured while loading yaml file: {e}')
        raise
    except Exception as e:
        logger.error(f'An Unexpected error occured while loading yaml file!')
            
    
def load_csv(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        logger.debug(f'Loading CSV file: {os.path.relpath(path=file_path, start=ROOT_DIR)}')
        df = pd.read_csv(file_path)
        logger.debug('File Successfully loaded!')
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('An Unexpected error occurred while loading the data: %s', e)
        raise
        
