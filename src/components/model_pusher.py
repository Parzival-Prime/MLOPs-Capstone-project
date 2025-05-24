
from src.logger import logging
from src.cloud_storage.azure_storage import AzureBlobStorage
from src.entity.config_entity import ModelPusherConfig, ModelEvaluationConfig, ModelTrainerConfig
from src.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact

logger = logging.getLogger('Model Pusher')


class ModelPusher:
    def __init__(self, 
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig
                 ):
    
        self.model_trainer_artifact = model_trainer_artifact
        self.model_pusher_config = model_pusher_config
        
        
    def push_model(self) -> ModelPusherArtifact:
        """Push the trained model to Azure Blob Storage."""
        try:
            logger.info("Pushing model to Azure Blob Storage...")
            
            # Upload model to Azure Blob Storage
            blob_client = AzureBlobStorage()
            blob_client.upload_file(
                file_path=self.model_trainer_artifact.model_object_file_path,
                file_blob_path=self.model_pusher_config.model_blob_file_path,
                container_name=self.model_pusher_config.container_name,
                remove=False
                )
            
            # Create and return ModelPusherArtifact
            model_pusher_artifact = ModelPusherArtifact(
                model_blob_file_path=self.model_pusher_config.model_blob_file_path,
                container_name=self.model_pusher_config.container_name
                )
            
            logger.info("Model pushed successfully")
            return model_pusher_artifact
        except Exception as e:
            logger.error(f"Error occurred while pushing model to storage: {e}")
            raise 
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """Initiate the model pusher process."""
        try:
            logger.info("Initiating model pusher...")
            
            artifact = self.push_model()
            
            return artifact
        except Exception as e:
            logger.error(f"Error occurred during model pusher initiation: {e}")
            raise
        

def main():
    
    # Load configuration
    model_trainer_config = ModelTrainerConfig()
    model_trainer_artifact = ModelTrainerArtifact(model_object_file_path=model_trainer_config.model_object_file_path)
    model_pusher_config = ModelPusherConfig()
    
    # Create ModelPusher instance
    model_pusher = ModelPusher(
        model_trainer_artifact=model_trainer_artifact,
        model_pusher_config=model_pusher_config
    )
    
    # Initiate model pusher
    model_pusher.initiate_model_pusher()
    
if __name__ == "__main__":
    main()