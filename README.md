# AI-Powered Customer Retention & Churn Prediction System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-Model-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A production-ready machine learning system that predicts customer churn for a telecom provider and delivers real-time retention recommendations through an interactive Streamlit dashboard.

---

## Project Overview

Customer churn is one of the most costly problems in subscription-based businesses. This system uses the **IBM Telco Customer Churn** dataset to train multiple ML classifiers, identify at-risk customers, and surface actionable retention strategies — all through a clean, real-time web interface.

---

## Features

- **Real-time churn prediction** with probability scores and risk classification (Low / Medium / High)
- **Interactive Streamlit dashboard** with gauge charts, stacked bar charts, and customer financial profiles
- **Retention recommendation engine** that maps risk level to targeted strategies
- **Prediction history tracking** within the session
- **Modular ML pipeline** with preprocessing, training, and serialization steps
- **Quick-fill sample customers** (Low / Medium / High risk) for instant demo

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.9+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Plotly, Power BI |
| App Framework | Streamlit |
| Model Serialization | Joblib |

---

## Models Used

| Model | Description |
|---|---|
| Logistic Regression | Baseline linear classifier |
| Random Forest | Ensemble tree-based model (default pipeline) |
| XGBoost | Gradient boosted trees for optimized performance |

---

## Model Performance

> Results on the IBM Telco Churn dataset (80/20 train-test split, stratified):

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | ~80% | ~65% | ~55% | ~60% |
| Random Forest | ~79% | ~63% | ~50% | ~56% |
| XGBoost | ~81% | ~67% | ~57% | ~62% |

---

## Project Structure

```
Customer-Retention-Churn-Prediction-System/
├── app/
│   ├── app.py                  # Streamlit dashboard
│   ├── recommendation_engine.py # Risk classification & retention strategies
│   └── utils.py                # Pipeline loader utility
├── data/
│   └── raw/
│       └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── models/
│   ├── churn_pipeline.pkl      # Trained sklearn pipeline (used by app)
│   ├── best_churn_model.pkl
│   ├── churn_prediction_model.pkl
│   └── scaler.pkl
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory Data Analysis
│   ├── 03_model_training.ipynb # Model training experiments
│   └── 04_model_optimization.ipynb
├── src/
│   └── pipeline_training.py   # End-to-end training script
├── assets/                    # Static assets (screenshots, icons)
├── main.py                    # Project entry point
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Nikhillokesh777/Customer-Retention-Churn-Prediction-System.git
cd Customer-Retention-Churn-Prediction-System

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Train the Model
```bash
python src/pipeline_training.py
```
This reads `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`, trains the pipeline, and saves `models/churn_pipeline.pkl`.

### Launch the Streamlit App
```bash
streamlit run app/app.py
```
Open `http://localhost:8501` in your browser.

---

## Future Improvements

- [ ] Add SHAP explainability for individual predictions
- [ ] Integrate XGBoost and Logistic Regression into the app as selectable models
- [ ] Add batch prediction via CSV upload
- [ ] Deploy to AWS (EC2 / Elastic Beanstalk) or Streamlit Cloud
- [ ] Connect Power BI dashboard via REST API
- [ ] Add unit tests with `pytest`

---

## Dataset

**IBM Telco Customer Churn** — publicly available on [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).  
7,043 customers × 21 features including demographics, account info, and subscribed services.

---

## License

This project is licensed under the [MIT License](LICENSE).
