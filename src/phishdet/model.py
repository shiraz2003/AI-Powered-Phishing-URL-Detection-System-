from __future__ import annotations
import logging
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, Tuple
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)
SEED = 42
MODEL_FILENAME = "phishing_model.joblib"
VECTORIZER_FILENAME = "tfidf_vectorizer.joblib"

def split_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    X = df["url"].values
    y = df["label"].values
    
    splitter1 = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=SEED)
    train_idx, temp_idx = next(splitter1.split(X, y))
    X_train, y_train = X[train_idx], y[train_idx]
    X_temp, y_temp = X[temp_idx], y[temp_idx]  # ← FIXED: Define y_temp FIRST
    
    splitter2 = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=SEED)
    val_idx, test_idx = next(splitter2.split(X_temp, y_temp))
    
    train_df = pd.DataFrame({"url": X_train, "label": y_train})
    val_df = pd.DataFrame({"url": X_temp[val_idx], "label": y_temp[val_idx]})
    test_df = pd.DataFrame({"url": X_temp[test_idx], "label": y_temp[test_idx]})
    
    print(f"Dataset split: train={len(train_df)}, val={len(val_df)}, test={len(test_df)}")
    return train_df, val_df, test_df


def train_model(df: pd.DataFrame) -> Dict[str, float]:
    train_df, val_df, test_df = split_dataset(df)
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X_train = vectorizer.fit_transform(train_df["url"].tolist())
    X_val = vectorizer.transform(val_df["url"].tolist())
    X_test = vectorizer.transform(test_df["url"].tolist())
    y_train = train_df["label"].values
    y_val = val_df["label"].values
    y_test = test_df["label"].values
    clf = LogisticRegression(solver="liblinear", max_iter=5000, random_state=SEED, class_weight='balanced')
    print("Training LogisticRegression model...")
    clf.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, clf.predict(X_train))
    val_acc = accuracy_score(y_val, clf.predict(X_val))
    test_acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Train acc: {train_acc:.3f}, Val acc: {val_acc:.3f}, Test acc: {test_acc:.3f}")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(clf, models_dir / MODEL_FILENAME)
    joblib.dump(vectorizer, models_dir / VECTORIZER_FILENAME)
    print(f"Saved model to {models_dir / MODEL_FILENAME}")
    return {
        "model_type": "LogisticRegression",
        "training_accuracy": float(train_acc),
        "validation_accuracy": float(val_acc),
        "test_accuracy": float(test_acc),
        "feature_size": X_train.shape[1],
    }

def load_model():
    models_dir = Path("models")
    model_path = models_dir / MODEL_FILENAME
    vec_path = models_dir / VECTORIZER_FILENAME
    if not model_path.exists() or not vec_path.exists():
        raise FileNotFoundError(f"Model files not found in {models_dir}. Run train first.")
    clf = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return clf, vectorizer

def predict_url(url: str):
    clf, vectorizer = load_model()
    X = vectorizer.transform([url])
    proba = clf.predict_proba(X)[0, 1]  # Probability of phishing (label=1)
    label = int(proba >= 0.5)
    return label, float(proba)
