.

 AI-Powered Phishing URL Detection System

A Machine Learning based phishing URL detection system that identifies malicious URLs using Logistic Regression + TF-IDF vectorization.

The model is trained on the PhiUSIIL Phishing URL Dataset and achieves ~98% accuracy on the test set.

This project provides a CLI-based interface for predicting phishing URLs individually or in batches.

✨ Features

✅ Detect phishing URLs with 98% accuracy
✅ Single URL prediction from command line
✅ Batch prediction using CSV files
✅ Fast TF-IDF feature extraction
✅ Production-ready model saved with Joblib
✅ Simple CLI interface using Click

📊 Model Performance
Dataset	Accuracy
Train	99.6%
Validation	98.0%
Test	98.0%

Label Encoding

0 = Benign URL
1 = Phishing URL
📦 Project Structure
phishing-url-detector/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv
│
├── src/
│   └── phishdet/
│       ├── cli.py
│       ├── model.py
│       ├── data.py
│       └── models/
│           └── phishing_model.joblib
│
└── test_urls_sample.csv
⚙️ Installation

Clone the repository

git clone https://github.com/yourusername/phishing-url-detector.git
cd phishing-url-detector

Install dependencies

pip install pandas scikit-learn click joblib numpy

Or using requirements file

pip install -r requirements.txt
📥 Dataset

Download the PhiUSIIL Phishing URL Dataset and place it in:

data/PhiUSIIL_Phishing_URL_Dataset.csv

Dataset Source:

https://archive.ics.uci.edu/ml/index.php

🚀 Training the Model

Navigate to the src directory and run:

cd src
python -m phishdet.cli train --data ../data/PhiUSIIL_Phishing_URL_Dataset.csv

This will:

Load the dataset

Train the TF-IDF + Logistic Regression model

Save the trained model in:

src/phishdet/models/
🔍 Predicting URLs
Single URL Prediction
python -m phishdet.cli predict --url "http://paypal.com.fake-login.ru"

Example Output

URL: http://paypal.com.fake-login.ru
Prediction: 🟥 PHISHING
Probability: 0.8923
Batch URL Prediction

You can analyze multiple URLs using a CSV file.

Input File (test_urls.csv)
url
https://www.google.com
http://paypal.com.fake-login.ru

Run prediction:

python -m phishdet.cli predict-file --input test_urls.csv --output results.csv
Output File (results.csv)
url,prediction,phishing_probability,status
https://www.google.com,0,0.12,✅ BENIGN
http://paypal.com.fake-login.ru,1,0.92,🟥 PHISHING
🖥 CLI Commands

Show help menu

python -m phishdet.cli --help

Available commands:

train                     Train phishing detection model
predict --url <URL>       Predict a single URL
predict-file              Batch prediction using CSV
🧠 Model Architecture

The detection pipeline uses:

1️⃣ TF-IDF Vectorization

Converts URLs into numerical features based on character patterns.

2️⃣ Logistic Regression

A fast and interpretable classifier that performs well on text-based data.

Pipeline:

URL → TF-IDF Vectorizer → Logistic Regression → Prediction
🧪 Sample Test File

Example file included:

test_urls_sample.csv

You can modify it to test your own URLs.
