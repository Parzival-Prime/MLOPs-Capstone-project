# promote model

import os
import mlflow
from mlflow.exceptions import RestException

def promote_model():

    dagshub_username = os.getenv("DAGSHUB_USERNAME")
    dagshub_token = os.getenv("DAGSHUB_TOKEN")

    assert dagshub_username is not None, "DAGSHUB_USERNAME not found in env"
    assert dagshub_token is not None, "DAGSHUB_TOKEN not found in env"

    mlflow.set_tracking_uri(f"https://{dagshub_username}:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow")

    model_name = 'imdb_sentiment_model3'    
    
    client = mlflow.MlflowClient()
    
    staging_version = client.get_model_version_by_alias(name=model_name, alias='challenger')
    
    try:
        production_version = client.get_model_version_by_alias(name=model_name, alias='alpha')
    except RestException:
        print('There is no model in production currently!')
    else:
        client.set_registered_model_alias(
            name=model_name,
            version=production_version.version,
            alias='veteran'
        )
    finally:
        client.set_registered_model_alias(
            name=model_name,
            version=staging_version.version,
            alias='alpha'
        )
        
    print(f"Challenger Model promoted to Alpha")

if __name__ == "__main__":
    promote_model()