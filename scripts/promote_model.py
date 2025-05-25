# promote model

import os
import mlflow

def promote_model():

    dagshub_username = os.getenv("DAGSHUB_USERNAME")
    dagshub_token = os.getenv("DAGSHUB_TOKEN")

    assert dagshub_username is not None, "DAGSHUB_USERNAME not found in env"
    assert dagshub_token is not None, "DAGSHUB_TOKEN not found in env"

    mlflow.set_tracking_uri(f"https://{dagshub_username}:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow")

    model_name = 'imdb_sentiment_model'    
    
    client = mlflow.MlflowClient()
    
    latest_version_staging = client.get_latest_versions(model_name, stages=['staging'])[0].version
    
    prod_versions = client.get_latest_versions(model_name, stages=['Production'])
    
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage='Archived'
        )
    
    client.transition_model_stage(
        name=model_name,
        version=latest_version_staging,
        stage='Prdoduction'
    )
    
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()