import os
import pickle
import mlflow
import mlflow.sklearn as mlsk

# dagshub_username = os.getenv("DAGSHUB_USERNAME")
dagshub_token = os.getenv("DAGSHUB_TOKEN")

# assert dagshub_username is not None, "DAGSHUB_USERNAME not found in env"
assert dagshub_token is not None, "DAGSHUB_TOKEN not found in env"

mlflow.set_tracking_uri(f"https://Parzival-Prime:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow")

model_name = 'imdb_sentiment_model3'

model_version = client = mlflow.MlflowClient()
production_version = client.get_model_version_by_alias(name=model_name, alias='alpha')
run_id = production_version.run_id
model_uri = f'runs:/{run_id}/model'
model = mlsk.load_model(model_uri)

os.makedirs('models', exist_ok=True)

with open('models/model.pkl', 'wb') as file:
    pickle.dump(model, file)
    






