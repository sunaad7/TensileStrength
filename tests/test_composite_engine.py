"""
TensileCheckmate: Comprehensive Test & Debug Suite
Validates micromechanics equations, ML simulation pipeline, figure generation,
and presentation deck structure.
"""

import os
import pytest
import numpy as np
import pandas as pd
from pptx import Presentation
from pptx.util import Inches

from src.micromechanics import (
    ConstituentProperties,
    volume_to_weight_fraction,
    classical_rule_of_mixtures,
    modified_rule_of_mixtures,
    composite_elastic_moduli,
    generate_stress_strain_data
)
from src.ml_models import generate_synthetic_dataset, train_and_evaluate_models
from src.plotting_ml import generate_all_ml_figures


class TestMicromechanics:
    """Unit tests for composite micromechanics and physics equations."""

    def test_volume_to_weight_fraction_conservation(self):
        props = ConstituentProperties(rho_f=2.58, rho_m=1.18)
        for vf in [0.10, 0.30, 0.50, 0.60, 0.70]:
            res = volume_to_weight_fraction(vf, props)
            assert pytest.approx(res["V_f"] + res["V_m"], 1e-6) == 1.0
            assert pytest.approx(res["W_f"] + res["W_m"], 1e-6) == 1.0
            assert pytest.approx(res["weight_percent_fiber"] + res["weight_percent_matrix"], 1e-6) == 100.0
            assert res["rho_c"] > props.rho_m
            assert res["rho_c"] < props.rho_f

    def test_reference_vf_0_50_weight_fraction(self):
        props = ConstituentProperties(rho_f=2.58, rho_m=1.18)
        res = volume_to_weight_fraction(0.50, props)
        # At Vf = 0.50, Wf should be approx 68.6%
        assert pytest.approx(res["weight_percent_fiber"], abs=0.2) == 68.62
        assert pytest.approx(res["rho_c"], abs=0.01) == 1.88

    def test_classical_rule_of_mixtures_milestones(self):
        props = ConstituentProperties(sigma_fu=3400.0, sigma_mu=70.0)
        # Slide 18 milestones:
        # Vf = 0.10 -> 403 MPa
        # Vf = 0.30 -> 1069 MPa
        # Vf = 0.50 -> 1735 MPa
        # Vf = 0.60 -> 2068 MPa
        assert pytest.approx(classical_rule_of_mixtures(0.10, props), abs=1.0) == 403.0
        assert pytest.approx(classical_rule_of_mixtures(0.30, props), abs=1.0) == 1069.0
        assert pytest.approx(classical_rule_of_mixtures(0.50, props), abs=1.0) == 1735.0
        assert pytest.approx(classical_rule_of_mixtures(0.60, props), abs=1.0) == 2068.0

    def test_halpin_tsai_moduli_bounds(self):
        props = ConstituentProperties(E_f=72400.0, E_m=3400.0)
        for vf in [0.20, 0.40, 0.50, 0.60]:
            mod = composite_elastic_moduli(vf, props)
            # E1 (Voigt upper bound) must exceed E2 (Halpin-Tsai)
            assert mod["E_1_MPa"] > mod["E_2_MPa"]
            # E2 must exceed neat resin modulus
            assert mod["E_2_MPa"] > props.E_m
            # Poisson ratio bounds
            assert 0.20 < mod["nu_12"] < 0.40

    def test_modified_rule_of_mixtures_factors(self):
        props = ConstituentProperties(sigma_fu=3400.0, sigma_mu=70.0)
        res = modified_rule_of_mixtures(
            V_f=0.50,
            void_content=0.015,
            misalignment_deg=2.0,
            weibull_bundle_factor=0.63,
            interface_efficiency=0.95,
            props=props
        )
        assert 0.0 < res["eta_theta"] <= 1.0
        assert 0.0 < res["eta_v"] <= 1.0
        assert 0.0 < res["eta_w"] <= 1.0
        assert 0.0 < res["eta_int"] <= 1.0
        assert res["sigma_c_modified"] < res["sigma_c_ideal"]
        assert 30.0 < res["knockdown_percentage"] < 50.0

    def test_stress_strain_curve_properties(self):
        props = ConstituentProperties(sigma_fu=3400.0, sigma_mu=70.0)
        data = generate_stress_strain_data(V_f=0.50, props=props)
        comp = data["composite"]
        # Must have positive failure strain and peak stress
        assert data["peak_stress_MPa"] > 800.0
        assert data["failure_strain_pct"] > 2.0
        # Check brittle drop: last stress point must drop to 0
        assert comp["stress_MPa"][-1] == 0.0

    def test_invalid_fiber_volume_fraction_raises_error(self):
        props = ConstituentProperties()
        for invalid_vf in [-0.1, -1.0, 1.05, 2.5]:
            with pytest.raises(ValueError, match="between 0.0 and 1.0"):
                volume_to_weight_fraction(invalid_vf, props)
            with pytest.raises(ValueError, match="between 0.0 and 1.0"):
                classical_rule_of_mixtures(invalid_vf, props)
            with pytest.raises(ValueError, match="between 0.0 and 1.0"):
                modified_rule_of_mixtures(invalid_vf, props=props)
            with pytest.raises(ValueError, match="between 0.0 and 1.0"):
                composite_elastic_moduli(invalid_vf, props)

    def test_invalid_void_content_raises_error(self):
        with pytest.raises(ValueError, match="Void content"):
            modified_rule_of_mixtures(0.50, void_content=-0.05)
        with pytest.raises(ValueError, match="Void content"):
            modified_rule_of_mixtures(0.50, void_content=1.2)


class TestMLSimulationPipeline:
    """Unit tests for data generation, train/test split, and ML algorithms."""

    def test_synthetic_dataset_dimensions_and_ranges(self, tmp_path):
        csv_file = str(tmp_path / "test_sim.csv")
        df = generate_synthetic_dataset(n_samples=600, random_seed=42, output_path=csv_file)
        
        assert len(df) == 600
        assert df["Fiber_Volume_Fraction"].between(0.30, 0.60).all()
        assert df["Cure_Temperature_C"].between(80.0, 140.0).all()
        assert df["Pressure_MPa"].between(0.20, 1.00).all()
        assert (df["Tensile_Strength_MPa"] > 400.0).all()
        assert (df["Tensile_Strength_MPa"] < 2200.0).all()
        assert df.isnull().sum().sum() == 0

    def test_train_test_split_shapes(self):
        res = train_and_evaluate_models()
        assert res["X_train"].shape == (480, 4)
        assert res["X_test"].shape == (120, 4)
        assert len(res["y_train"]) == 480
        assert len(res["y_test"]) == 120

    def test_model_metrics_sanity(self):
        res = train_and_evaluate_models()
        metrics = res["metrics_table"].set_index("Model")
        
        # RoM baseline should show negative R2 on uncalibrated synthetic data
        assert metrics.loc["Rule of Mixtures (Physics Baseline)", "R2"] < 0.0
        assert metrics.loc["Rule of Mixtures (Physics Baseline)", "MAE_MPa"] > 300.0
        
        # All three ML models should achieve R2 >= 0.80
        assert metrics.loc["Linear Regression", "R2"] >= 0.80
        assert metrics.loc["Random Forest (300 trees)", "R2"] >= 0.80
        assert metrics.loc["Gradient Boosting", "R2"] >= 0.80

    def test_ml_prediction_inference(self):
        res = train_and_evaluate_models()
        models = res["models"]
        # Arbitrary single sample: Vf=0.45, T=115C, P=0.6 MPa, RoM=1568.5 MPa
        sample = np.array([[0.45, 115.0, 0.60, 1568.5]])
        for name in ["lr", "rf", "gb"]:
            pred = models[name].predict(sample)[0]
            assert 800.0 < pred < 1400.0


class TestFiguresAndArtifacts:
    """Verify that all figures and presentation decks exist, are non-empty, and valid."""

    def test_all_8_figures_exist_and_non_empty(self):
        expected_figs = [
            "figures/fig1_rom_ideal_curve.png",
            "figures/fig2_ply_structure_schematic.png",
            "figures/fig3_stress_strain_schematic.png",
            "figures/fig4_why_strength_falls_short.png",
            "figures/fig5_combining_physics_ml.png",
            "figures/fig6_train_test_workflow.png",
            "figures/fig7_model_comparison_r2.png",
            "figures/fig8_predicted_vs_actual.png"
        ]
        for f in expected_figs:
            assert os.path.exists(f), f"Missing figure: {f}"
            assert os.path.getsize(f) > 50000, f"Figure too small or corrupted: {f}"

    def test_expanded_27_slide_presentation_structure(self):
        pptx_path = "Composites_ML_Tensile_Strength_expanded.pptx"
        assert os.path.exists(pptx_path), "Missing 27-slide presentation deck"
        prs = Presentation(pptx_path)
        
        # Exactly 27 slides
        assert len(prs.slides) == 27
        
        # 16:9 widescreen dimensions
        assert pytest.approx(prs.slide_width.inches, 0.01) == 13.333
        assert pytest.approx(prs.slide_height.inches, 0.01) == 7.500
        
        # Verify notes on every slide
        for i, slide in enumerate(prs.slides, start=1):
            assert slide.has_notes_slide, f"Slide {i} missing notes slide"
            note_text = slide.notes_slide.notes_text_frame.text.strip()
            assert len(note_text) > 10, f"Slide {i} has empty speaker notes"

    def test_dataset_csv_files_exist(self):
        assert os.path.exists("data/synthetic_composite_dataset.csv")
        assert os.path.exists("data/published_experimental_data.csv")
        
        df_syn = pd.read_csv("data/synthetic_composite_dataset.csv")
        assert len(df_syn) == 600
        
        df_exp = pd.read_csv("data/published_experimental_data.csv")
        assert len(df_exp) >= 16

    def test_slide_shape_bounds_no_overflow(self):
        prs = Presentation("Composites_ML_Tensile_Strength_expanded.pptx")
        slide_w = prs.slide_width.inches
        slide_h = prs.slide_height.inches
        tolerance = 0.05
        
        for idx, slide in enumerate(prs.slides, start=1):
            for shape in slide.shapes:
                if shape.left is not None and shape.width is not None:
                    right = shape.left.inches + shape.width.inches
                    assert right <= slide_w + tolerance, (
                        f"Slide {idx} shape '{shape.name}' overflows width: {right:.2f} > {slide_w:.2f}"
                    )
                if shape.top is not None and shape.height is not None:
                    bottom = shape.top.inches + shape.height.inches
                    assert bottom <= slide_h + tolerance, (
                        f"Slide {idx} shape '{shape.name}' overflows height: {bottom:.2f} > {slide_h:.2f}"
                    )

    def test_presentation_script_integrity(self):
        script_path = "presentation_script.md"
        assert os.path.exists(script_path), "Missing presentation_script.md"
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        for i in range(1, 28):
            assert f"Slide {i}:" in content, f"Missing Slide {i} in presentation script"
        
        # Verify defense Q&A section
        assert "Likely Questions and Short Answers" in content
        assert "Q1:" in content
        assert "Q2:" in content
        assert "Q3:" in content
        assert "Q4:" in content

    def test_report_md_integrity(self):
        report_path = "REPORT.md"
        assert os.path.exists(report_path), "Missing REPORT.md"
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "Executive Summary" in content
        assert "Rule of Mixtures" in content
        assert "Machine Learning" in content
        assert "Random Forest" in content
        assert "Gradient Boosting" in content
        assert "Linear Regression" in content
        assert "$R^2$" in content or "R^2" in content or "R²" in content

