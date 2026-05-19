"""
AI-Powered Customer Retention & Churn Prediction System
Entry point — trains the pipeline and launches the Streamlit app.
"""
import subprocess
import sys


def train():
    print("Training churn prediction pipeline...")
    subprocess.run([sys.executable, "src/pipeline_training.py"], check=True)
    print("Training complete. Model saved to models/churn_pipeline.pkl")


def run_app():
    print("Launching Streamlit dashboard...")
    subprocess.run(["streamlit", "run", "app/app.py"], check=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Churn Prediction System")
    parser.add_argument(
        "--mode",
        choices=["train", "app"],
        default="app",
        help="'train' to retrain the model, 'app' to launch the dashboard (default: app)",
    )
    args = parser.parse_args()

    if args.mode == "train":
        train()
    else:
        run_app()
