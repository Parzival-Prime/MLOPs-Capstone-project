from src.cloud_storage.azure_storage import AzureBlobStorage
from src.constants import ROOT_DIR

import os

blob_service_client = AzureBlobStorage()


# creating blob container
# blob_service_client.create_container('models')

# uploading a file
blob_service_client.download_file(file_save_path=os.path.join(ROOT_DIR, 'models', 'temp.txt'), file_blob_path=os.path.join('models/temp.txt'), container_name='models')
