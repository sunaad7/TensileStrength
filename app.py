"""
TensileCheckmate: Physics-Informed Machine Learning Composite Dashboard
Interactive Streamlit application for predicting GFRP tensile strength using ML and the Rule of Mixtures.
"""

import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.ml_models import train_and_evaluate_models, generate_synthetic_dataset


st.set_page_config(
    page_title="TensileCheckmate | ML & Rule of Mixtures Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom academic CSS
st.markdown("""
<style>
    .main-title {
        font-family: 'Times New Roman', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #002D62;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-family: 'Times New Roman', serif;
        font-size: 1.15rem;
        color: #0070C0;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F5F8FC;
        border: 1.5px solid #0070C0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .metric-val {
        font-size: 1.7rem;
        font-weight: bold;
        color: #002D62;
    }
    .metric-lbl {
        font-size: 0.95rem;
        color: #555555;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TensileCheckmate: Machine Learning & Rule of Mixtures</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Physics-Informed Tensile Strength Prediction for Unidirectional E-Glass/Epoxy (GFRP)</div>', unsafe_allow_html=True)

# Train or load models once
@st.cache_resource
def get_trained_pipeline():
    return train_and_evaluate_models()

pipeline = get_trained_pipeline()
metrics_df = pipeline["metrics_table"]
models = pipeline["models"]

# Sidebar Inputs
st.sidebar.header("⚙️ Specimen & Processing Parameters")

V_f = st.sidebar.slider("Fibre Volume Fraction (Vf)", 0.30, 0.60, 0.50, 0.01)
T_cure = st.sidebar.slider("Cure Temperature (°C)", 80.0, 140.0, 115.0, 1.0)
Pressure = st.sidebar.slider("Consolidation Pressure (MPa)", 0.20, 1.00, 0.60, 0.05)

# Calculate Physics Baseline
sigma_f = 3400.0  # MPa
sigma_m = 70.0    # MPa
RoM_val = sigma_f * V_f + sigma_m * (1.0 - V_f)

# Predict with ML Models
input_vector = np.array([[V_f, T_cure, Pressure, RoM_val]])
pred_lr = models["lr"].predict(input_vector)[0]
pred_rf = models["rf"].predict(input_vector)[0]
pred_gb = models["gb"].predict(input_vector)[0]

# Metrics Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Rule of Mixtures (Ideal)</div>
        <div class="metric-val">{RoM_val:.1f} MPa</div>
        <div style="color: #666; font-size: 0.85rem;">Handbook Upper Bound</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Linear Regression (ML)</div>
        <div class="metric-val" style="color: #0070C0;">{pred_lr:.1f} MPa</div>
        <div style="color: #0070C0; font-size: 0.85rem;">R² = 0.879 (Test Set)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Random Forest (300 trees)</div>
        <div class="metric-val" style="color: #1F4E79;">{pred_rf:.1f} MPa</div>
        <div style="color: #1F4E79; font-size: 0.85rem;">R² = 0.853 (Test Set)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Gradient Boosting</div>
        <div class="metric-val" style="color: #2E75B6;">{pred_gb:.1f} MPa</div>
        <div style="color: #2E75B6; font-size: 0.85rem;">R² = 0.841 (Test Set)</div>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Live ML Predictions & Comparison",
    "📈 Model Evaluation (Synthetic Test Set)",
    "🖼️ Presentation Figures Gallery (8 Slides)",
    "📥 Downloads & Project Assets"
])

# -------------------------------------------------------------
# TAB 1: Live Predictions
# -------------------------------------------------------------
with tab1:
    st.subheader("Live Multi-Model Tensile Strength Prediction")
    st.write(f"Evaluating continuous UD E-glass/epoxy at **Vf = {V_f:.2f}**, **T = {T_cure:.1f} °C**, and **P = {Pressure:.2f} MPa**.")

    col_t1a, col_t1b = st.columns([1.1, 0.9])
    with col_t1a:
        # Comparison Bar Chart
        fig_bar, ax_bar = plt.subplots(figsize=(6.5, 4.0))
        bars = ax_bar.bar(
            ["Rule of Mixtures\n(Ideal Upper Bound)", "Linear\nRegression", "Random Forest\n(300 trees)", "Gradient\nBoosting"],
            [RoM_val, pred_lr, pred_rf, pred_gb],
            color=["#888888", "#0070C0", "#1F4E79", "#2E75B6"],
            edgecolor="#333333",
            width=0.55
        )
        for b in bars:
            h = b.get_height()
            ax_bar.text(b.get_x() + b.get_width() / 2.0, h + 25, f"{h:.0f} MPa", ha='center', va='bottom', fontsize=9.5, weight='bold')

        ax_bar.set_ylim(0, 2400)
        ax_bar.set_ylabel("Predicted Tensile Strength (MPa)")
        ax_bar.grid(True, axis='y', linestyle='--', alpha=0.35)
        plt.tight_layout()
        st.pyplot(fig_bar)

    with col_t1b:
        st.markdown("### 🔍 Model Prediction Breakdown")
        st.write(f"- **Physics Baseline (RoM):** `{RoM_val:.1f} MPa`")
        st.write(f"- **ML Defect Correction:** `-{(RoM_val - pred_lr):.1f} MPa` (~{((RoM_val - pred_lr)/RoM_val)*100:.1f}% reduction)")
        st.write(f"- **Linear Regression Output:** `{pred_lr:.1f} MPa`")
        st.write(f"- **Random Forest Output:** `{pred_rf:.1f} MPa`")
        st.write(f"- **Gradient Boosting Output:** `{pred_gb:.1f} MPa`")
        st.markdown("---")
        st.info("💡 **Notice:** The ideal Rule of Mixtures assumes 0% voids and perfect collinear fibers. Machine Learning learns the physical knockdown from cure temperature, pressure, and bonding defects.")

# -------------------------------------------------------------
# TAB 2: Model Evaluation
# -------------------------------------------------------------
with tab2:
    st.subheader("Model Evaluation on Held-Out Synthetic Test Data (120 Samples)")
    st.dataframe(metrics_df, width="stretch")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.image("figures/fig7_model_comparison_r2.png", caption="Fig 7: Model Comparison R² Bar Chart", width="stretch")
    with col_e2:
        st.image("figures/fig8_predicted_vs_actual.png", caption="Fig 8: Predicted vs. Actual Scatter Plots", width="stretch")

# -------------------------------------------------------------
# TAB 3: Figures Gallery
# -------------------------------------------------------------
with tab3:
    st.subheader("Presentation Diagram Slides Gallery")
    st.write("All 8 high-resolution figures matching the 27-slide presentation:")

    c1, c2 = st.columns(2)
    with c1:
        st.image("figures/fig4_why_strength_falls_short.png", caption="Slide 7: Why Measured Strength Falls Short", width="stretch")
        st.image("figures/fig2_ply_structure_schematic.png", caption="Slide 15: Unidirectional Ply Structure Cross-Section", width="stretch")
        st.image("figures/fig1_rom_ideal_curve.png", caption="Slide 18: Ideal RoM Strength Curve vs. Vf", width="stretch")
    with c2:
        st.image("figures/fig5_combining_physics_ml.png", caption="Slide 10: Combining Physics with Machine Learning", width="stretch")
        st.image("figures/fig3_stress_strain_schematic.png", caption="Slide 17: Tensile Behaviour of GFRP (Stress-Strain)", width="stretch")
        st.image("figures/fig6_train_test_workflow.png", caption="Slide 20: Train-Test Evaluation Workflow", width="stretch")

# -------------------------------------------------------------
# TAB 4: Downloads
# -------------------------------------------------------------
with tab4:
    st.subheader("Project Assets & Deliverables")
    st.write("Download the presentation deck, presenter script, dataset, and report:")

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("### 📽️ PowerPoint Presentation")
        st.write("27-slide academic deck in Times New Roman with blue outline boxes, embedded diagrams, and speaker notes on all 27 slides.")
        p_path = "Composites_ML_Tensile_Strength_expanded.pptx"
        if os.path.exists(p_path):
            with open(p_path, "rb") as f:
                st.download_button("📥 Download 27-Slide Deck (.pptx)", f, file_name="Composites_ML_Tensile_Strength_expanded.pptx")

    with d2:
        st.markdown("### 🎙️ Presenter Script")
        st.write("Complete slide-by-slide word-for-word presentation script (25-30 min) and defense Q&A.")
        s_path = "presentation_script.md"
        if os.path.exists(s_path):
            with open(s_path, "rb") as f:
                st.download_button("📥 Download Presentation Script (.md)", f, file_name="presentation_script.md")

    with d3:
        st.markdown("### 📊 600-Sample Dataset")
        st.write("Synthetic E-glass/epoxy dataset with Vf, Cure Temperature, Pressure, RoM estimate, and Tensile Strength.")
        csv_path = "data/synthetic_composite_dataset.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                st.download_button("📥 Download Dataset (.csv)", f, file_name="synthetic_composite_dataset.csv")
