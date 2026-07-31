
<img src="frontend/assets/banner.png" alt="Cancer Subtype Discovery Banner" width="100%"/>

# Cancer Subtype Discovery

### Unsupervised ML | K-Means Clustering | TCGA Pan-Cancer RNA-Seq

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

<br/>

**[Live Demo](https://cancer-subtype-discovery-5z5ftcx4mxvri6raw9mcox.streamlit.app/) · [API Docs](https://cancer-subtype-discovery.onrender.com/docs) · [Backend](https://cancer-subtype-discovery.onrender.com) · [GitHub](https://github.com/mushahidhussainleel) · [LinkedIn](https://linkedin.com/in/mushahid-hussain-dev)**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Cancer Subtypes](#cancer-subtypes)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [ML Pipeline](#ml-pipeline)
- [Model Performance](#model-performance)
- [Key Findings](#key-findings)
- [API Endpoints](#api-endpoints)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [Visualizations](#visualizations)
- [Medical Disclaimer](#medical-disclaimer)
- [Developer](#developer)

---

## Overview

**Cancer Subtype Discovery** is an end-to-end unsupervised machine learning project that identifies natural cancer subtype groupings from high-dimensional gene expression data — without using any labels during training.

Built on the **TCGA Pan-Cancer RNA-Seq dataset** (UCI ML Repository), this project demonstrates a complete unsupervised ML pipeline covering EDA, dimensionality reduction with PCA, clustering with K-Means, model evaluation, FastAPI backend, and Streamlit frontend deployment.

The core challenge: **801 patients, 20,531 gene features** — finding natural biological groupings using only gene expression patterns.

> **Note:** This project is built for educational and portfolio purposes. It demonstrates real-world unsupervised ML engineering including dimensionality reduction, clustering evaluation, and API deployment.

---

## Cancer Subtypes

| Code | Full Name | Cluster | Patients |
|------|-----------|---------|----------|
| BRCA | Breast Invasive Carcinoma | 4 | 300 |
| KIRC | Kidney Renal Clear Cell Carcinoma | 2 | 146 |
| LUAD | Lung Adenocarcinoma | 3 | 141 |
| PRAD | Prostate Adenocarcinoma | 0 | 136 |
| COAD | Colon Adenocarcinoma | 1 | 78 |

---

## Project Structure

```
cancer-subtype-discovery/
│
├── backend/
│   ├── data/
│   │   ├── raw/
│   │   │   ├── data.csv              # TCGA RNA-Seq data (801 x 20531) — not tracked
│   │   │   └── labels.csv            # Cancer type labels — not tracked
│   │   └── processed/
│   │       └── data_processed.csv    # PCA-transformed data (801 x 262) — not tracked
│   │
│   ├── notebooks/
│   │   ├── 01_EDA.ipynb                           # Exploratory Data Analysis
│   │   ├── 02_Dimensionality_Reduction(PCA).ipynb # PCA + Scaling
│   │   └── 03_Clustering_and_Model_Selection.ipynb # Clustering + Evaluation
│   │
│   ├── model/
│   │   ├── kmeans_model.pkl          # Trained K-Means (k=5)
│   │   ├── pca_model.pkl             # Fitted PCA (262 components)
│   │   └── scaler.pkl                # Fitted StandardScaler
│   │
│   ├── api/
│   │   ├── main.py                   # FastAPI app + 3 endpoints
│   │   ├── schemas.py                # Pydantic output schema + cluster mapping
│   │   ├── predict.py                # ML pipeline — scale → PCA → predict
│   │   └── home.html                 # Landing page HTML
│   │
│   ├── images/                       # All EDA and clustering visualizations
│   │   ├── cancer_distribution.png
│   │   ├── feature_distribution.png
│   │   ├── pca_explained_variance.png
│   │   ├── pca_scatter.png
│   │   ├── elbow_method.png
│   │   ├── kmeans_clusters.png
│   │   └── dendrogram.png
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                        # Streamlit frontend
│   ├── requirements.txt
│   └── assets/
│       ├── banner.png                # Project banner
│       └── sample_patient.csv        # Demo CSV — 1 patient, 20531 genes
│
├── .gitignore
└── README.md
```

---

## Tech Stack

### Machine Learning
| Library | Purpose |
|---------|---------|
| Scikit-learn | StandardScaler, PCA, KMeans, metrics |
| SciPy | Hierarchical clustering, dendrogram |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Joblib | Model serialization |
| Matplotlib / Seaborn | EDA and clustering visualizations |

### Backend
| Library | Purpose |
|---------|---------|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Output validation |

### Frontend & Deployment
| Tool | Purpose |
|------|---------|
| Streamlit | Interactive frontend UI |
| Render | Backend cloud deployment |
| Streamlit Cloud | Frontend deployment |
| GitHub | Version control |

---

## ML Pipeline

```
Raw Data (801 x 20531 genes)
        |
01_EDA.ipynb
  |-- Data Loading & Cleaning (drop sample ID column)
  |-- Missing Values Check -> 0 missing
  |-- Duplicate Check -> 0 duplicates
  |-- Basic Statistics (zero-variance genes identified)
  |-- Cancer Type Distribution (BRCA dominant ~37%)
  |-- Feature Distribution + Skewness (-0.35 mild left skew)
  |-- Observation: Data already log-normalized
        |
02_Dimensionality_Reduction(PCA).ipynb
  |-- StandardScaler (mean=0, std=1)
  |-- PCA Full Fit -> Explained Variance Analysis
  |-- Optimal Components: 262 (85% variance retained)
  |-- PCA Transform: 20531 -> 262 dimensions
  |-- 2D Scatter: KIRC perfectly separated, BRCA/PRAD/LUAD overlap
  |-- Save: data_processed.csv, scaler.pkl, pca_model.pkl
        |
03_Clustering_and_Model_Selection.ipynb
  |-- Elbow Method -> k=5 confirmed
  |-- K-Means (k=5): Silhouette 0.167, DB 2.369
  |-- Cluster Visualization with Centroids
  |-- Hierarchical Clustering + Dendrogram (Ward method)
  |-- DBSCAN Evaluation -> Failed (3 clusters, 582 noise points)
  |-- Model Selection -> K-Means (predict() capability)
  |-- Cluster Profiling -> Cancer type mapping confirmed
  |-- Save: kmeans_model.pkl
        |
FastAPI Backend
  |-- predict.py -> scale -> PCA -> KMeans predict
  |-- schemas.py -> cluster mapping (0-4 to cancer types)
  |-- main.py -> /, /model-info, /predict endpoints
        |
Streamlit Frontend
  |-- app.py -> CSV upload -> API call -> result display
```

---

## Model Performance

### Algorithm Comparison

| Algorithm | Silhouette Score | Davies-Bouldin | Clusters Found | predict() | Selected |
|-----------|-----------------|----------------|----------------|-----------|----------|
| **K-Means** | **0.167** | **2.369** | **5** | **Yes** | **Yes** |
| Hierarchical | 0.168 | 2.362 | 5 | No | No |
| DBSCAN | N/A | N/A | 3 (582 noise) | No | No |

**K-Means selected** as final model — `predict()` capability required for FastAPI real-time inference.

> Moderate scores are expected for 262-dimensional biological data. Gene expression clustering is inherently challenging due to biological overlap between cancer types.

### Cluster Profiling

| Cluster | Cancer Type | Correct | Total | Purity |
|---------|------------|---------|-------|--------|
| 0 | PRAD | 134 | 135 | 99.3% |
| 1 | COAD | 74 | 74 | 100% |
| 2 | KIRC | 145 | 145 | 100% |
| 3 | LUAD | 141 | 214 | 65.9% |
| 4 | BRCA | 232 | 233 | 99.6% |

---

## Key Findings

- **KIRC** is the most distinctly separated cancer type in gene expression space — K-Means captured it with 100% purity. KIRC patients show a completely different gene expression profile from all other cancer types.
- **COAD** also achieved 100% cluster purity despite being the smallest group (78 patients).
- **BRCA, PRAD, LUAD** overlap in PCA space — reflecting real biological similarity in gene expression patterns between these cancer types.
- **PCA** reduced dimensions from **20,531 to 262** retaining **85% variance** — making clustering computationally feasible without significant information loss.
- **DBSCAN failed** on this dataset — confirming that gene expression data lacks clear density clusters in high-dimensional space (curse of dimensionality).
- **Skewness of -0.35** confirmed that data is already well log-normalized — no additional transformation needed.

---

## API Endpoints

Base URL: `https://cancer-subtype-discovery.onrender.com`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Landing page (HTML) |
| `GET` | `/model-info` | Model details and cluster mapping |
| `POST` | `/predict` | Upload CSV — get cancer subtype prediction |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

### Sample Request

```bash
curl -X POST "https://cancer-subtype-discovery.onrender.com/predict" \
  -F "file=@sample_patient.csv"
```

### Sample Response

```json
{
  "cluster_id": 2,
  "cancer_type": "KIRC",
  "full_name": "Kidney Renal Clear Cell Carcinoma",
  "description": "Kidney cancer subtype detected based on gene expression pattern.",
  "disclaimer": "This tool is intended for research and educational purposes only..."
}
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- Conda or venv
- Git

### 1. Clone Repository

```bash
git clone https://github.com/mushahidhussainleel/cancer-subtype-discovery.git
cd cancer-subtype-discovery
```

### 2. Create Virtual Environment

```bash
conda create -n cancer_env python=3.11
conda activate cancer_env
```

### 3. Run Backend

```bash
cd backend/api
pip install -r ../requirements.txt
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 4. Run Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at: `http://localhost:8501`

> **Note:** Update `API_URL` in `frontend/app.py` to `http://127.0.0.1:8000` for local testing.

---

## Deployment

### Backend — Render

| Setting | Value |
|---------|-------|
| Runtime | Python 3 |
| Root Directory | `backend/api` |
| Build Command | `pip install -r ../requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port 10000` |

### Frontend — Streamlit Cloud

| Setting | Value |
|---------|-------|
| Repository | `mushahidhussainleel/cancer-subtype-discovery` |
| Branch | `main` |
| Main file path | `frontend/app.py` |

---

## Visualizations

### Cancer Type Distribution
![Cancer Distribution](backend/images/cancer_distribution.png)

### PCA Explained Variance (85% Threshold)
![PCA Variance](backend/images/pca_explained_variance.png)

### PCA Scatter Plot — Cancer Types
![PCA Scatter](backend/images/pca_scatter.png)

### Elbow Method — Optimal K Selection
![Elbow](backend/images/elbow_method.png)

### K-Means Clustering Results with Centroids
![K-Means](backend/images/kmeans_clusters.png)

### Hierarchical Clustering Dendrogram
![Dendrogram](backend/images/dendrogram.png)

---

## Medical Disclaimer

> This project is intended for **research and educational purposes only**.
> It is **not a substitute** for professional medical diagnosis or advice.
> Predictions are based on unsupervised machine learning trained on research data
> and may not reflect clinical ground truth.
> Always consult a qualified healthcare provider for medical decisions.

---

## Developer

<div align="center">

**Mushahid Hussain**

Python Backend Developer | ML Practitioner

[![LinkedIn](https://img.shields.io/badge/LinkedIn-mushahid--hussain--dev-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mushahid-hussain-dev)
[![GitHub](https://img.shields.io/badge/GitHub-mushahidhussainleel-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mushahidhussainleel)
[![Email](https://img.shields.io/badge/Email-mushahidh442007@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mushahidh442007@gmail.com)

</div>

---

<div align="center">

If this project helped you, please give it a star!

Made with dedication by **Mushahid Hussain**

</div>
