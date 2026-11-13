# TensileCheckmate: Predicting Tensile Strength of E-Glass Fibre/Epoxy Composite (GFRP) Using Machine Learning and the Rule of Mixtures

**Course:** Fundamentals of Composite Materials  
**Project Focus:** Physics-Informed Machine Learning for Composite Mechanical Property Prediction  
**Material System:** Unidirectional E-Glass Reinforcement in Diglycidyl Ether of Bisphenol-A (DGEBA) Epoxy Matrix  
**Dataset:** 600 Simulated Specimens (80/20 Train/Test Split, Random Seed = 42)  
**Models Evaluated:** Rule of Mixtures Baseline, Linear Regression, Random Forest (300 Trees), Gradient Boosting  
**Deliverables:** 27-Slide PowerPoint Deck (`Composites_ML_Tensile_Strength_expanded.pptx`), Full Script (`presentation_script.md`), Technical Report (`REPORT.md`), Interactive Dashboard (`app.py`)  

---

## 🎯 Executive Overview

Physical tensile testing of GFRP via ASTM D3039 is expensive, slow, and difficult to scale across varying fibre fractions and cure conditions. Analytical formulas like the **Rule of Mixtures (RoM)** provide an instantaneous physics-based estimate:

$$\sigma_{c,\text{ideal}} = \sigma_f V_f + \sigma_m (1 - V_f)$$

However, the textbook formula ignores voids, fiber misalignment, imperfect interfacial bonding, and cure kinetics.

**TensileCheckmate** combines analytical mechanics with machine learning:
1. **Engineered Physics Input:** The Rule of Mixtures estimate is used as an explicit input feature alongside fibre volume fraction ($V_f$), cure temperature ($T$), and consolidation pressure ($P$).
2. **Synthetic Simulation Dataset:** 600 specimens are generated with physical void reduction and cure kinetics degradation, plus 3% experimental testing scatter.
3. **Machine Learning Models:** Linear Regression, Random Forest (300 trees), and Gradient Boosting are trained on 480 samples and scored on 120 held-out test samples.
4. **Key Finding:** While the uncalibrated Rule of Mixtures alone yields $R^2 = -0.898$ (predicting worse than the mean), machine learning models explain **84% to 88%** of the variation on the synthetic test set ($R^2 = 0.88$ for Linear Regression, $0.85$ for Random Forest, and $0.84$ for Gradient Boosting).

---

## 📁 Repository Structure

```
TensileCheckmate/
├── Composites_ML_Tensile_Strength_expanded.pptx  # 27-slide deck (Times New Roman, #0070C0, embedded figures, notes on all slides)
├── presentation_script.md                       # Word-for-word spoken presenter script (27 slides) + defense Q&A
├── REPORT.md                                    # Comprehensive technical project report
├── app.py                                       # Interactive Streamlit web application & live ML predictor
├── generate_all.py                              # Master build script: runs simulation, trains ML, builds figures & PPTX
├── generate_presentation_27slides.py             # Programmatic builder for the 27-slide PowerPoint deck
├── data/
│   ├── synthetic_composite_dataset.csv          # 600 simulated specimens (Vf, Cure Temp, Pressure, RoM, Strength)
│   └── published_experimental_data.csv          # 16 published literature benchmark datasets
├── src/
│   ├── ml_models.py                             # Simulation generator, train/test split, LR, RF, GB models
│   ├── plotting_ml.py                           # High-DPI figure generator for all 8 presentation diagrams
│   ├── micromechanics.py                        # Constituent properties and analytical formulas
│   └── sensitivity.py                           # Parametric sensitivity engine
└── figures/                                     # 8 Publication-grade 300 DPI figures
    ├── fig1_rom_ideal_curve.png                 # Slide 18: Ideal RoM strength curve vs. Vf
    ├── fig2_ply_structure_schematic.png         # Slide 15: UD ply cross-section (fibers in epoxy matrix)
    ├── fig3_stress_strain_schematic.png         # Slide 17: Schematic stress-strain curve (brittle fracture)
    ├── fig4_why_strength_falls_short.png        # Slide 7: Why measured strength falls short (4 factors)
    ├── fig5_combining_physics_ml.png            # Slide 10: Combining physics with ML architecture
    ├── fig6_train_test_workflow.png             # Slide 20: Train-test workflow (600 samples, 80/20 split)
    ├── fig7_model_comparison_r2.png             # Slide 22: Model comparison R² bar chart
    └── fig8_predicted_vs_actual.png             # Slide 23: Predicted vs. Actual strength scatter plots
```

---

## 🚀 Quickstart & Commands

### 1. Run Complete Master Build
To regenerate the dataset, train models, render all 8 figures, and build the 27-slide presentation:
```powershell
python generate_all.py
```

### 2. Launch Interactive Web Dashboard
To run the live prediction tool and explore parameter sliders:
```powershell
streamlit run app.py
```

### 3. Generate Slides Individually
```powershell
python generate_presentation_27slides.py
```

---

## 📊 Summary of Simulation Results (Test Set: N = 120, Seed = 42)

| Model Name | $R^2$ Score | RMSE (MPa) | MAE (MPa) | Model Type |
| :--- | :---: | :---: | :---: | :--- |
| **Rule of Mixtures Alone** | **$-0.898$** | **$383.4$** | **$362.9$** | Analytical Baseline (No ML) |
| **Linear Regression** | **$0.879$** | **$104.2$** | **$82.5$** | Physics-Informed ML |
| **Random Forest (300 trees)** | **$0.853$** | **$114.6$** | **$89.9$** | Ensemble ML |
| **Gradient Boosting** | **$0.841$** | **$118.2$** | **$93.4$** | Boosting Ensemble |
