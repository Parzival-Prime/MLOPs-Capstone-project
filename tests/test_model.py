import unittest
import mlflow
import os
import mlflow.tracing
import mlflow.tracking
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


class TestModelLoading(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        dagshub_token = os.getenv('DAGSHUB_TOKEN')
        dagshub_username = os.getenv('DAGSHUB_USERNAME')
        
        assert dagshub_token is not None, "DAGSHUB_TOKEN env variable not found! "
        assert dagshub_username is not None, "DAGSHUB_USERNAME env variable not found!"
        
        mlflow.set_tracking_uri(f'https://{dagshub_username}:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow')
        mlflow.set_registry_uri(f'https://{dagshub_username}:{dagshub_token}@dagshub.com/Parzival-Prime/MLOPs-Capstone-project.mlflow')
        
        # Load the new model from MLflow model registry
        print('MLflow Connection Successful!')
        print('Loading Model...')
        client = mlflow.tracking.MlflowClient()
        staging_version = client.get_model_version_by_alias(name='imdb_sentiment_model3', alias='challenger')
        staging_version.run_id
        logged_model = f'runs:/{staging_version.run_id}/model'

        # Load model as a PyFuncModel.
        cls.new_model = mlflow.pyfunc.load_model(logged_model)
        print('Model loaded!')
        
        print('Loading vectorizer...')
        # load vectorizer
        with open('models/vectorizer.pkl', 'rb') as file: 
            cls.vectorizer = pickle.load(file)
        print('Vectorizer loaded!')
        
        print('Loading test data...')
        # load holdout test
        cls.holdout_data = pd.read_csv('artifact/feature/test.csv')
        print('Test data loaded!')
        

    def test_model_loaded_properly(self):
        self.assertIsNotNone(self.new_model)

    def test_model_signature(self):
        # Create a dummy input for the model based on expected input shape
        input_text = "hi how are you"
        input_data = self.vectorizer.transform([input_text])
        input_df = pd.DataFrame(input_data.toarray(), columns=[str(i) for i in range(input_data.shape[1])])

        # Predict using the new model to verify the input and output shapes
        prediction = self.new_model.predict(input_df)

        # Verify the input shape
        self.assertEqual(input_df.shape[1], len(self.vectorizer.get_feature_names_out()))

        # Verify the output shape (assuming binary classification with a single output)
        self.assertEqual(len(prediction), input_df.shape[0])
        self.assertEqual(len(prediction.shape), 1)  # Assuming a single output column for binary classification

    def test_model_performance(self):
        # Extract features and labels from holdout test data
        X_holdout = self.holdout_data.iloc[:,0:-1]
        y_holdout = self.holdout_data.iloc[:,-1]

        # Predict using the new model
        y_pred_new = self.new_model.predict(X_holdout)

        # Calculate performance metrics for the new model
        accuracy_new = accuracy_score(y_holdout, y_pred_new)
        precision_new = precision_score(y_holdout, y_pred_new)
        recall_new = recall_score(y_holdout, y_pred_new)
        f1_new = f1_score(y_holdout, y_pred_new)

        # Define expected thresholds for the performance metrics
        expected_accuracy = 0.40
        expected_precision = 0.40
        expected_recall = 0.40
        expected_f1 = 0.40

        # Assert that the new model meets the performance thresholds
        self.assertGreaterEqual(accuracy_new, expected_accuracy, f'Accuracy should be at least {expected_accuracy}')
        self.assertGreaterEqual(precision_new, expected_precision, f'Precision should be at least {expected_precision}')
        self.assertGreaterEqual(recall_new, expected_recall, f'Recall should be at least {expected_recall}')
        self.assertGreaterEqual(f1_new, expected_f1, f'F1 score should be at least {expected_f1}')

if __name__ == "__main__":
    unittest.main()