import os
import pickle
import json

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score

import mlflow
import mlflow.sklearn
import dagshub

from src.logger import logging
from src.utils import load_binary, load_csv, save_json
from src.exception import handle_exception, CustomException
from src.constants import DAGSHUB_REPO_NAME, DAGSHUB_REPO_OWNER, DAGSHUB_URL
from src.entity.config_entity import ModelTrainerConfig, ModelEvaluationConfig, FeatureEngineeringConfig
from src.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact, FeatureEngineeringArtifact

logger = logging.getLogger('Model Evaluation')

dagshub_username = os.getenv("DAGSHUB_USERNAME")
dagshub_token = os.getenv("DAGSHUB_TOKEN")

assert dagshub_username is not None, "DAGSHUB_USERNAME not found in env"
assert dagshub_token is not None, "DAGSHUB_TOKEN not found in env"

mlflow.set_tracking_uri(f"https://{dagshub_username}:{dagshub_token}@dagshub.com/{DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO_NAME}.mlflow")


class ModelEvaluation:
    
    def __init__(self, 
                 model_trainer_artifact: ModelTrainerArtifact, 
                 feature_engineering_artifact: FeatureEngineeringArtifact, 
                 model_evaluation_config: ModelEvaluationConfig=ModelEvaluationConfig()
                 ):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact = model_trainer_artifact
        self.feature_engineering_artifact = feature_engineering_artifact
        
    
    def evaluate_model(self, model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """Evaluate the model and return the evaluation metrics."""
        try:
            logger.info('Predicting the X_test Samples...')
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            logger.info('Prediction done.')
            logger.info('Calculating Metrics...')
            
            accuracy = accuracy_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_pred_proba)
            
            metrics_dict = {
                'accuracy': accuracy,
                'recall': recall,
                'precision': precision,
                'auc': auc
            }
            
            logging.info('Model Evaluation Metrics Calculated')
            
            return metrics_dict
        except Exception as e:
            logger.error(f'Error occured during Evaluating Metrics: {e}')
            raise
        
    def register_model(self, model_name: str, model_info: dict) -> None:
        """Register the model in MLflow."""
        try:
            logger.info(f'Registering model {model_name}...')
            model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"
            
            model_version = mlflow.register_model(model_uri=model_uri, name=model_name)
            
            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=model_version.version,
                stage=self.model_evaluation_config.model_stage
            )
            
            logger.info(f'Model {model_name} registered with version {model_version.version}.')
        except Exception as e:
            logger.error(f'Error occured during model registration: {e}')
            raise
        
    
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """Initiates Model Evaluation"""
        
        mlflow.set_experiment("My-DVC-Pipeline")
        with mlflow.start_run() as run:
            try:    
                logger.info('Loading Model and Test Data...')
                model = load_binary(file_path=self.model_trainer_artifact.model_object_file_path)
                test_data = load_csv(file_path=self.feature_engineering_artifact.featured_test_data_file_path)
                
                X_test = test_data.iloc[:, :-1].values
                y_test = test_data.iloc[:, -1].values
                
                metrics = self.evaluate_model(model=model, X_test=X_test, y_test=y_test)
                
                logger.debug('Saving metrics file...')
                save_json(dictionary=metrics, file_path=self.model_evaluation_config.metrics_file_path)
                
                logger.debug('Logging metrics to mlflow...')
                for metric_name, metric_value in metrics.items():
                    mlflow.log_metric(metric_name, metric_value)
                    
                logger.debug('Logging model parameter to mlflow...')
                if hasattr(model, 'get_params'):
                    params = model.get_params()
                    for param_name, param_value in params.items():
                        mlflow.log_param(param_name, param_value)
                        
                logger.debug('Logging model to mlflow...')
                mlflow.sklearn.log_model(model, 'model')
                
                
                logger.debug('Saving experiment info file...')
                model_info = {'run_id': run.info.run_id, 'model_path': self.model_evaluation_config.models_dir}
                save_json(dictionary=model_info, file_path=self.model_evaluation_config.experiment_info_file_path)
                
                logger.debug('Registering model...')
                self.register_model(model_name=self.model_evaluation_config.model_name, model_info=model_info)
                logger.info(f'Model registered with name: {self.model_evaluation_config.model_name}')
                
                logger.debug('Logging Model Evaluation artifact...')
                mlflow.log_artifact(self.model_evaluation_config.metrics_file_path)
                
                logger.info('Model Evaluation Completed Successfully')
                model_evaluation_artifact = ModelEvaluationArtifact(
                    metrics_file_path=self.model_evaluation_config.metrics_file_path,
                    experiment_info_file_path=self.model_evaluation_config.experiment_info_file_path
                )
                
                return model_evaluation_artifact
            except Exception as e:
                logger.error(f'Error occured in initiate_model_evaluation(): {e}')
                raise
    
    
def main():
    try:
        model_trainer_config = ModelTrainerConfig()
        model_trainer_artifact = ModelTrainerArtifact(
            model_object_file_path=model_trainer_config.model_object_file_path
        )
        
        feature_engineering_config = FeatureEngineeringConfig()
        feature_engineering_artifact = FeatureEngineeringArtifact(
            featured_train_data_file_path=feature_engineering_config.featured_train_data_file_path,
            featured_test_data_file_path=feature_engineering_config.featured_test_data_file_path,
            vectorizer_file_path=feature_engineering_config.vectorizer_file_path,
        )
        model_evaluation_config = ModelEvaluationConfig()
        
        model_evaluation = ModelEvaluation(
            model_trainer_artifact=model_trainer_artifact,
            feature_engineering_artifact=feature_engineering_artifact,
            model_evaluation_config=model_evaluation_config,
        )
        
        model_evaluation.initiate_model_evaluation()
    except Exception as e:
        logger.error(f'Error occured in model_evaluation main(): {e}')
        raise
    
if __name__ == "__main__":
    main()