import os
import pickle
import yaml
import json

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
        
def load_binary(file_path: str) -> object:
    """Loads object using pickle"""
    try:
        logger.debug(f'Loading object from {os.path.relpath(path=file_path, start=ROOT_DIR)}')
        with open(file=file_path, mode='rb') as obj:
            object_file = pickle.load(file=obj)
        
        logger.debug('Object loaded successfully!')
        return object_file
    except FileNotFoundError as e:
        logger.error(f'File {os.path.relpath(path=file_path, start=ROOT_DIR)} not found!')
        raise
        
    except Exception as e:
        logger.error(f'An Unexpected error occured in load_binary() function: {e}')
        raise
    
    
def save_json(dictionary: dict, file_path: str):
    """Saves json file into specified directory."""
    try:
        logger.debug(f'Saving json file {os.path.relpath(file_path, ROOT_DIR)}')
        with open(file_path, 'w') as file:
            json.dump(obj=dictionary, fp=file, indent=4)   
            
        logger.debug('File saved successfully!') 
    except json.JSONDecodeError as e:
        logger.error(f'Error occured while decoding file: {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected Error occured!')
        raise
    