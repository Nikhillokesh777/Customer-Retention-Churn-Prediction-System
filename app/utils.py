import joblib
import os

# Resolve path relative to this file so it works from any working directory
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_PATH  = os.path.join(BASE_DIR, "models", "churn_pipeline.pkl")


def load_pipeline():
    if not os.path.exists(PIPELINE_PATH):
        raise FileNotFoundError(
            f"Pipeline not found at {PIPELINE_PATH}. "
            "Run src/pipeline_training.py first."
        )
    return joblib.load(PIPELINE_PATH)
