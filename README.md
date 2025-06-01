
# 🧠 Sentiment Analysis Pipeline – MLOps Capstone

## 📌 Overview

This project is a production-grade Machine Learning pipeline built for sentiment analysis. It serves as a hands-on capstone to master MLOps principles, CI/CD automation, scalable model deployment, and observability practices. The primary goal is to emulate real-world, industry-standard workflows and get deep exposure to technologies like Docker, Kubernetes, and Azure.

---

## 🎯 Objectives

* Implement an end-to-end ML pipeline using MLOps best practices.
* Gain experience in:

  * Data and experiment versioning
  * CI/CD for ML workflows
  * Cloud-native model deployment
  * Monitoring with Prometheus and Grafana

---

## 🧰 Tech Stack

| Purpose             | Tool/Technology                    |
| ------------------- | ---------------------------------- |
| Code Versioning     | GitHub                             |
| Data Versioning     | DVC                                |
| Experiment Tracking | MLflow, DagsHub                    |
| Cloud Storage       | Azure Blob Storage                 |
| CI/CD               | GitHub Actions                     |
| Containerization    | Docker (Multi-stage builds)        |
| Image Optimization  | Distroless (experimental)          |
| Orchestration       | Kubernetes (AKS)                   |
| Monitoring          | Prometheus & Grafana               |
| Logging             | Python’s built-in `logging` module |

---

## 📁 Project Structure

```plaintext
.
├── .github/
│   └── workflows/
│       └── ci_cd_pipeline.yml      # CI/CD definition
├── data/
├── models/
├── notebooks/
├── artifacts/
├── src/
│  ├── components/
│     ├── data_ingestion.py
│     ├── data_transformation.py
│     ├── data_validation.py
│     ├── feature_engineering.py
│     ├── model_training.py
│     ├── model_evaluation.py
│     └── model_pusher.py
│
│   ├── configurations/
│     └── azure_blob_connection.py
│
│   ├── constants/
│      └── constants.py                # Centralized constants
│
│   ├── entities/
│      ├── config_entity.py
│      └── artifact_entity.py         # Uses `@dataclass`
│
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── deployments.yaml               # Kubernetes deployment + service
├── dvc.yaml                       # DVC pipeline definition
├── project.toml
└── setuptools.py
```

---

## ⚙️ Functionality Highlights

* **Pipeline Stages**: Modularized and organized under `components/`.
* **Version Control**: All pipeline stages, configs, and outputs tracked with DVC and GitHub.
* **Experiment Tracking**: Seamlessly integrated with MLflow (hosted on DagsHub).
* **Dockerization**: Built multi-stage Dockerfiles to reduce image size. Also explored distroless images.
* **CI/CD**: Automates testing, building, pushing Docker images, and deploying to AKS using GitHub Actions.
* **Monitoring**: Set up Prometheus and Grafana inside the cluster (under a dedicated `monitoring` namespace) to monitor application and cluster health.

---

## 📈 Lessons Learned

* **Logging**: A favorite part—Python’s built-in module was extensively used for modular and traceable logging.
* **Distroless Docker**: Explored but found it unnecessarily complex compared to its limited benefits.
* **CI/CD Debugging**: Took around 48 iterations to finalize a robust pipeline.
* **Kubernetes Monitoring**: Learned to configure Prometheus and Grafana on AKS, useful for production-grade observability.

---

## 🚀 Getting Started

### Run Locally

```bash
# Clone the repo
git clone <repo-url>
cd <repo-name>

# Create and activate a conda env
conda create -n sentiment-mlops python=3.9 -y
conda activate sentiment-mlops

# Install dependencies
pip install -r requirements.txt

# Reproduce pipeline
dvc repro
```

### Deploy to AKS

Ensure the CI/CD pipeline is correctly configured and push to the `main` branch:

```bash
git add .
git commit -m "Trigger CI/CD"
git push origin main
```

---

## 📊 Monitoring Dashboard

* Prometheus: Available inside `monitoring` namespace
* Grafana: Default dashboard imported with pod metrics
* Access:

  ```bash
  kubectl port-forward svc/grafana -n monitoring 3000:3000
  ```

---

## ✅ Conclusion

This project reflects a real-world ML production pipeline integrating modern tooling and best practices in data science engineering. It provided a strong foundation for implementing MLOps workflows with reproducibility, traceability, scalability, and observability. (Good Performance was not the aim of this project, though I am going to work on those in near future)

---
