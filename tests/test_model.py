import unittest
import mlflow
import os
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score


class TestModelLoading(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        dagshub_token = os.getenv('DAGSHUB_TOKEN')
        dagshub_username = os.getenv('DAGSHUB_USERNAME')
        
        assert dagshub_token is not None, "DAGSHUB_TOKEN env variable not found! "
        assert dagshub_username is not None, "DAGSHUB_USERNAME env variable not found!"
        
        mlflow.set_tracking_uri(f'https://{dagshub_username}:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow')
        
        # Load the new model from MLflow model registry
        cls.new_model_name = 'imdb_sentiment_model'
        cls.new_model_verion = cls.get_latest_model_version(cls.new_model_name)
        cls.new_model_uri = f'models:/{cls.new_model_name}/{cls.new_model_verion}'
        cls.new_model = mlflow.pyfunc.load_model(cls.new_model_uri)
        
        # load vectorizer
        cls.vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
        
        # load holdout test
        cls.holdout_data = pd.read_csv('artifact/feature/test.csv')
        
    @staticmethod
    def get_latest_model_version(model_name, stage='Staging'):
        client = mlflow.MlflowClient()
        latest_version = client.get_latest_versions(model_name, stage=[stage])
        return latest_version[0].version if latest_version else None
    
    def test_model_loaded_properly(self):
        self.assertIsNotNone(self.new_model)
    
    def test_model_signature(self):
        input_text = "you are ethereal my love"
        input_data = self.vectorizer.transform([input_text])
        input_df = pd.DataFrame(input_data.toarray(), columns=[str(i) for i in range(input_data.shape[1])])
        
        prediction = self.new_model.predict(input_df)
        
        self.assertEqual(input_df.shape[1], len(self.vectorizer.get_feature_names_out()))
        self.assertEqual(len(prediction), input_df.shape[0])
        self.assertEqual(len(prediction), 1)
        
    def test_model_performance(self):
        
        X_holdout = self.holdout_data.iloc[:, :-1]
        y_holdout = self.holdout_data.iloc[:, -1]
        
        y_pred_new = self.new_model.predict(X_holdout)
        y_pred_proba_new = self.new_model.predict_proba(X_holdout)
        
        accuracy_new = accuracy_score(y_holdout, y_pred_new)
        recall_new = recall_score(y_holdout, y_pred_new)
        precision_new = precision_score(y_holdout, y_pred_new)
        auc_new = roc_auc_score(y_holdout, y_pred_proba_new)
        
        expected_accuracy = 0.40
        expected_recall = 0.40
        expected_precision = 0.40
        expected_auc = 0.40
        
        self.assertGreater(accuracy_new, expected_accuracy, f'Accuracy should be greater than {expected_accuracy}')
        self.assertGreater(recall_new, expected_recall, f"Recall should be greater than {expected_recall}")
        self.assertGreater(precision_new, expected_precision, f"Precision should be greater than {expected_precision}")
        self.assertGreater(auc_new, expected_auc, f"Auc should be greater than {expected_auc}")
        
if __name__=='__main__':
    unittest.main()