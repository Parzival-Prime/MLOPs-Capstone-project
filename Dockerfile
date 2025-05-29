# //===================== Distroless Image =====================//

#----------- Stage 1: Build ----------- #
FROM python:3.12-slim AS loader

WORKDIR /app

COPY flask_app/loader/ /app/

# Contains mlflow and pickle as deps
RUN pip install --no-cache-dir -r requirements.txt

ARG DAGSHUB_TOKEN

ENV DAGSHUB_TOKEN=${DAGSHUB_TOKEN}

# This python file loads latest model from dagshub into 'models/' directory
RUN python loader.py


# ----------- Stage 2: Distroless debugger ----------- #
FROM python:3.12-slim AS builder

WORKDIR /app

COPY flask_app/templates /app/templates

COPY flask_app/app.py /app/app.py

COPY flask_app/requirements.txt /app/requirements.txt

COPY models/vectorizer.pkl /app/models/vectorizer.pkl

COPY models/stopwords.pkl /app/models/stopwords.pkl

COPY --from=loader /app/models/model.pkl /app/models/model.pkl

RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model into deps
RUN python -m spacy download en_core_web_sm

CMD ["python", "app.py"]

# ----------- Stage 3: Distroless Final ----------- #
