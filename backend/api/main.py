from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .schemas import CancerOutput, CLUSTER_INFO
from .predict import predict_from_csv

BASE_DIR = Path(__file__).parent

description = """
## Cancer Subtype Discovery API

AI-powered API to identify cancer subtype from gene expression data.

**Pipeline:** StandardScaler → PCA (262 components) → K-Means Clustering

| Cluster | Cancer Type | Full Name |
|---------|------------|-----------|
| 0 | BRCA | Breast Invasive Carcinoma |
| 1 | KIRC | Kidney Renal Clear Cell Carcinoma |
| 2 | COAD | Colon Adenocarcinoma |
| 3 | LUAD | Lung Adenocarcinoma |
| 4 | PRAD | Prostate Adenocarcinoma |

**Dataset:** TCGA Pan-Cancer RNA-Seq (UCI ML Repository)
**Patients:** 801 | **Genes:** 20,531 | **PCA Components:** 262 | **Variance Retained:** 85%

> This tool is for research purposes only. Not a substitute for medical advice.
"""

app = FastAPI(
    title="Cancer Subtype Discovery API",
    description=description,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Endpoint 1: Home ─────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home():
    with open(BASE_DIR / "home.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ── Endpoint 2: Model Info ───────────────────────────────
@app.get("/model-info")
async def model_info():
    return {
        "model": "K-Means Clustering",
        "n_clusters": 5,
        "pca_components": 262,
        "variance_retained": "85%",
        "input_features": 20531,
        "dataset": "TCGA Pan-Cancer RNA-Seq (UCI ML Repository)",
        "patients": 801,
        "cancer_types": CLUSTER_INFO,
        "evaluation": {
            "silhouette_score": 0.167,
            "davies_bouldin_score": 2.369
        },
        "note": "Moderate scores are expected for 262-dimensional gene expression data."
    }

# ── Endpoint 3: Predict ──────────────────────────────────
@app.post("/predict", response_model=CancerOutput)
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        file_bytes = await file.read()
        cluster_id = predict_from_csv(file_bytes)
        info = CLUSTER_INFO[cluster_id]

        return CancerOutput(
            cluster_id=cluster_id,
            cancer_type=info["cancer_type"],
            full_name=info["full_name"],
            description=info["description"],
            disclaimer="⚠️ This tool is for research purposes only. "
                      "It is not a substitute for professional medical diagnosis. "
                      "Always consult a qualified healthcare provider."
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")