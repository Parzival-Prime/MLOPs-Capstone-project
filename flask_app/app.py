from flask import Flask, render_template, request
import pickle
import re
import string
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time
import spacy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    "app_request_count", "Total number of requests to the app", ["method", "endpoint"], registry=registry
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Latency of requests in seconds", ["endpoint"], registry=registry
)

PREDICTION_COUNT = Counter(
    "model_prediction_count", "Count of predictions for each class", ["prediction"], registry=registry
)
    
with open('models/model.pkl', 'rb') as file:
    model = pickle.load(file)
    
with open('models/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)
    
with open('models/stopwords.pkl', 'rb') as file:
    stopwords = pickle.load(file)
    
def preprocess_text(text):
    """Helper function to preprocess a single text string."""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", ' ', text)
    text = text.replace('؛', "")
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    text = ' '.join([token.lemma_ for token in nlp(text)])
    
    return text
    
def inference_preprocess(text):
    text = preprocess_text(text)
    features = vectorizer.transform([text])
    features_array = features.toarray()
    assert features_array.shape[1] == 20, f"Expected 20 features, got {features_array.shape[1]}"
    return features_array





@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    start_time=time.time()
    response = render_template('index.html', result=None)
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
    return response


@app.route('/predict', methods=["POST"])
def predict():
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
    start_time = time.time()
    text = request.form['text']
    features_df = inference_preprocess(text)
    result = model.predict(features_df)
    prediction = result[0]
    
    PREDICTION_COUNT.labels(prediction=str(prediction)).inc()
    
    REQUEST_LATENCY.labels(endpoint='/predict').observe(time.time()-start_time)
    
    return render_template('index.html', result=prediction)


@app.route('/metrics', methods=['GET'])
def metrics():
    """Expose only custom Prometheus metrics."""
    return generate_latest(registry), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)