import joblib
import numpy as np
import pandas as pd
import io
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent / "model"

# Load models once at startup
scaler = joblib.load(MODEL_DIR / "scaler.pkl")
pca    = joblib.load(MODEL_DIR / "pca_model.pkl")
kmeans = joblib.load(MODEL_DIR / "kmeans_model.pkl")

def predict_from_csv(file_bytes: bytes) -> int:
    """
    Accept CSV file bytes → scale → PCA → predict cluster id.
    """
    df = pd.read_csv(io.BytesIO(file_bytes))

    # Drop sample ID column if present
    if df.shape[1] == 20532:
        df = df.drop(columns=[df.columns[0]])

    # Validate gene count
    if df.shape[1] != 20531:
        raise ValueError(f"Expected 20531 gene columns, got {df.shape[1]}")

    # Rename columns to match scaler training format
    df.columns = [f"gene_{i}" for i in range(20531)]

    # Pipeline: scale → PCA → predict
    X_scaled = scaler.transform(df)
    X_pca    = pca.transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(262)])
    cluster  = kmeans.predict(X_pca_df)

    return int(cluster[0])