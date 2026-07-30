from pydantic import BaseModel

# Cluster → Cancer Type mapping (derived from cluster profiling)
CLUSTER_INFO = {
    0: {
        "cancer_type": "PRAD",
        "full_name": "Prostate Adenocarcinoma",
        "description": "Prostate cancer subtype detected based on gene expression pattern."
    },
    1: {
        "cancer_type": "COAD",
        "full_name": "Colon Adenocarcinoma",
        "description": "Colon cancer subtype detected based on gene expression pattern."
    },
    2: {
        "cancer_type": "KIRC",
        "full_name": "Kidney Renal Clear Cell Carcinoma",
        "description": "Kidney cancer subtype detected based on gene expression pattern."
    },
    3: {
        "cancer_type": "LUAD",
        "full_name": "Lung Adenocarcinoma",
        "description": "Lung cancer subtype detected based on gene expression pattern."
    },
    4: {
        "cancer_type": "BRCA",
        "full_name": "Breast Invasive Carcinoma",
        "description": "Breast cancer subtype detected based on gene expression pattern."
    },
}

# Output schema
class CancerOutput(BaseModel):
    cluster_id: int
    cancer_type: str
    full_name: str
    description: str
    disclaimer: str