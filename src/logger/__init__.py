import os
import logging
from logging.handlers import RotatingFileHandler
from src.constants import ROOT_DIR, LOG_DIR, LOG_FILENAME, MAX_LOG_SIZE, BACKUP_COUNT


log_dir_path = os.path.join(ROOT_DIR, LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)


# Get specific loggers used by Azure SDK
azure_logger = logging.getLogger('azure')
azure_logger.setLevel(logging.WARNING)  # or ERROR to suppress more

http_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
http_logger.setLevel(logging.WARNING)

urllib_logger = logging.getLogger('urllib3')
urllib_logger.setLevel(logging.WARNING)

msal_logger = logging.getLogger('msal')
msal_logger.setLevel(logging.WARNING)

# Ensure all handlers attached to those loggers also suppress
for handler in azure_logger.handlers:
    handler.setLevel(logging.WARNING)

for handler in http_logger.handlers:
    handler.setLevel(logging.WARNING)

for handler in urllib_logger.handlers:
    handler.setLevel(logging.WARNING)
    
for handler in msal_logger.handlers:
    handler.setLevel(logging.WARNING)




def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    log_file_path = os.path.join(log_dir_path, LOG_FILENAME)
    
    formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
    
    filehandler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT) 
    filehandler.setFormatter(formatter)
    filehandler.setLevel(logging.DEBUG)
    
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(logging.INFO)
    
    logger.addHandler(filehandler)
    logger.addHandler(consolehandler)
    
configure_logger()