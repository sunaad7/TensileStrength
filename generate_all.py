"""
TensileCheckmate: Master Build Script for ML + Rule of Mixtures Project
Generates the 600-specimen dataset, renders 8 academic figures,
trains ML models, and builds Composites_ML_Tensile_Strength_expanded.pptx.
"""

import os
import sys

from src.ml_models import generate_synthetic_dataset, train_and_evaluate_models
from src.plotting_ml import generate_all_ml_figures
from generate_presentation_27slides import build_expanded_deck


def main():
    print("=" * 75)
    print("TENSILECHECKMATE: ML & RULE OF MIXTURES MASTER BUILD")
    print("=" * 75)

    print("\n[Step 1/4] Generating 600-specimen synthetic composite dataset...")
    df = generate_synthetic_dataset(output_path="data/synthetic_composite_dataset.csv")

    print("\n[Step 2/4] Training and evaluating Machine Learning models...")
    res = train_and_evaluate_models(dataset_path="data/synthetic_composite_dataset.csv")
    print("\n--- Simulation Results (Held-Out Test Set: N = 120, Seed = 42) ---")
    print(res["metrics_table"].to_string(index=False))
    print("-" * 70)

    print("\n[Step 3/4] Generating all 8 academic-grade figures...")
    generate_all_ml_figures()

    print("\n[Step 4/4] Building 27-slide presentation deck (Composites_ML_Tensile_Strength_expanded.pptx)...")
    build_expanded_deck("Composites_ML_Tensile_Strength_expanded.pptx")

    print("\n" + "=" * 75)
    print("MASTER BUILD COMPLETE!")
    print("Deck: Composites_ML_Tensile_Strength_expanded.pptx (27 slides, notes on all)")
    print("Script: presentation_script.md")
    print("Report: REPORT.md")
    print("Dataset: data/synthetic_composite_dataset.csv")
    print("=" * 75)


if __name__ == "__main__":
    main()
