import streamlit as st
import requests
import pandas as pd

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="Cancer Subtype Discovery",
    page_icon="🧬",
    layout="wide"
)

# ── Banner ───────────────────────────────────────────────
st.image("assets/banner.png", use_container_width=True)

# ── Title ────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center; color:#38bdf8;'>
        Cancer Subtype Discovery
    </h1>
    <p style='text-align:center; color:#94a3b8; font-size:16px;'>
        Upload a gene expression CSV file to identify cancer subtype
        using K-Means Clustering on TCGA Pan-Cancer RNA-Seq data.
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Layout: 2 columns ────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload Gene Expression File")
    st.markdown(
        "Upload a CSV file containing **20,531 gene expression values** "
        "for a single patient."
    )

    # Sample CSV download
    st.markdown("##### No data? Download sample file:")
    with open("assets/sample_patient.csv", "rb") as f:
        st.download_button(
            label="Download Sample CSV",
            data=f,
            file_name="sample_patient.csv",
            mime="text/csv"
        )

    st.markdown("---")

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="CSV must contain 20,531 gene expression columns"
    )

    predict_btn = st.button("Predict Cancer Subtype", type="primary")

with col2:
    st.markdown("### Prediction Result")

    if predict_btn:
        if uploaded_file is None:
            st.warning("Please upload a CSV file first.")
        else:
            with st.spinner("Analyzing gene expression data..."):
                try:
                    response = requests.post(
                        "https://cancer-subtype-discovery.onrender.com/predict",
                        files={"file": (uploaded_file.name,
                                       uploaded_file.getvalue(),
                                       "text/csv")},
                        timeout=60
                    )

                    if response.status_code == 200:
                        result = response.json()

                        st.success("Prediction Complete!")

                        st.markdown(f"""
                        <div style='background:#1e293b; padding:20px;
                                    border-radius:12px; border:1px solid #38bdf8;
                                    margin-top:10px;'>
                            <h2 style='color:#38bdf8; margin-bottom:5px;'>
                                {result['cancer_type']}
                            </h2>
                            <p style='color:#94a3b8; font-size:14px;
                                      margin-bottom:15px;'>
                                {result['full_name']}
                            </p>
                            <p style='color:#e2e8f0;'>{result['description']}</p>
                            <hr style='border-color:#334155; margin:15px 0;'>
                            <p style='color:#64748b; font-size:12px;'>
                                Cluster ID: {result['cluster_id']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div style='background:#1c1208; padding:15px;
                                    border-radius:10px; border:1px solid #92400e;
                                    margin-top:15px;'>
                            <p style='color:#d97706; font-size:12px;'>
                                <strong>Medical Disclaimer:</strong> {result['disclaimer']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    elif response.status_code == 422:
                        st.error("Invalid file format. Please ensure your CSV has exactly 20,531 gene columns.")
                    else:
                        st.error(f"Prediction failed. Please try again. (Error {response.status_code})")

                except requests.exceptions.Timeout:
                    st.error("Request timed out. The server may be starting up — please wait 30 seconds and try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the server. Please check your internet connection.")
                except Exception as e:
                    st.error("An unexpected error occurred. Please try again.")

    else:
        st.info("Upload a CSV file and click 'Predict Cancer Subtype' to get results.")

# ── Model Info Section ───────────────────────────────────
st.markdown("---")
st.markdown("### About the Model")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Patients", "801")
m2.metric("Gene Features", "20,531")
m3.metric("PCA Components", "262")
m4.metric("Cancer Subtypes", "5")

st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#475569; font-size:12px;'>
    Built by <strong style='color:#38bdf8'>Mushahid Hussain</strong> |
    HopeToSkills ML Program |
    FastAPI + K-Means + TCGA Pan-Cancer RNA-Seq
</p>
""", unsafe_allow_html=True)