# Technical Project Report: Predicting Tensile Strength of E-Glass Fibre/Epoxy Composite (GFRP) Using Machine Learning and the Rule of Mixtures

**Course:** Fundamentals of Composite Materials  
**Project Focus:** Physics-Informed Machine Learning for Composite Mechanical Property Prediction  
**Material System:** Unidirectional E-Glass Reinforcement in Diglycidyl Ether of Bisphenol-A (DGEBA) Epoxy Matrix  
**Dataset:** 600 Simulated Specimens (80/20 Train/Test Split, Random Seed = 42)  
**Models Evaluated:** Rule of Mixtures Baseline, Linear Regression, Random Forest (300 Trees), Gradient Boosting  
**Presenting Authors:** [Name], [Name], and [Name]  

---

## 1. Executive Summary

Determining the tensile strength of continuous unidirectional (UD) E-glass fibre reinforced epoxy composites (GFRP) through physical ASTM D3039 tensile coupon testing is expensive, destructive, and slow. While analytical models such as the classical **Rule of Mixtures (RoM)** provide an instantaneous physics-based estimate from fibre volume fraction ($V_f$) and constituent handbook strengths, they rely on idealized assumptions (perfect bonding, zero voids, perfectly straight fibres) and universally overestimate physical strength.

In this project, we develop a **hybrid physics-informed machine learning pipeline** that bridges analytical composite micromechanics with data-driven predictive modeling. Using a dataset of **600 simulated specimens** generated under realistic processing distributions ($V_f \in [0.30, 0.60]$, cure temperature $T \in [80, 140]^\circ\mathrm{C}$, and consolidation pressure $P \in [0.20, 1.00]\ \mathrm{MPa}$), we formulate four input features including the analytical Rule of Mixtures estimate:

$$\sigma_{c,\text{ideal}} = \sigma_f V_f + \sigma_m (1 - V_f)$$

The simulation target reflects physical strength degradation caused by process-induced voids and imperfect cure kinetics, superimposed with $3\%$ experimental testing scatter.

We train three distinct machine learning algorithms—**Linear Regression**, **Random Forest (300 trees)**, and **Gradient Boosting**—on $480$ training samples and evaluate their generalization on $120$ held-out test samples using $R^2$, Root Mean Squared Error (RMSE), and Mean Absolute Error (MAE).

### Key Findings:
- **Baseline Failure of Uncalibrated RoM:** Evaluated alone on the held-out test set, the Rule of Mixtures yields $R^2 = -0.898$, $\mathrm{RMSE} = 383.4\ \mathrm{MPa}$, and $\mathrm{MAE} = 362.9\ \mathrm{MPa}$. The negative $R^2$ demonstrates that an uncalibrated ideal formula performs worse than predicting the test set mean because it ignores microstructural defects.
- **Machine Learning Precision:** All three machine learning models effectively learn the defect corrections, explaining **$84\%$ to $88\%$** of the variation in the synthetic test set:
  - **Linear Regression:** $R^2 = 0.879$, $\mathrm{RMSE} = 104.2\ \mathrm{MPa}$, $\mathrm{MAE} = 82.5\ \mathrm{MPa}$
  - **Random Forest (300 trees):** $R^2 = 0.853$, $\mathrm{RMSE} = 114.6\ \mathrm{MPa}$, $\mathrm{MAE} = 89.9\ \mathrm{MPa}$
  - **Gradient Boosting:** $R^2 = 0.841$, $\mathrm{RMSE} = 118.2\ \mathrm{MPa}$, $\mathrm{MAE} = 93.4\ \mathrm{MPa}$
- **Pipeline Feasibility:** The close performance cluster of all three models demonstrates that embedding the physics-based Rule of Mixtures as an engineered feature allows lightweight linear regression to perform comparably to complex ensemble methods. 
- **Validation Caveat:** All evaluation results are established on synthetic simulation data designed to verify pipeline architecture. Physical laboratory testing is the required next step before industrial structural design adoption.

---

## 2. Theoretical Foundations & Problem Formulation

### 2.1 The Classical Rule of Mixtures (Voigt Model)
The classical parallel rule of mixtures assumes iso-strain deformation along the continuous fibre axis:

$$\epsilon_c = \epsilon_f = \epsilon_m$$

Static equilibrium on a representative transverse cross-section yields:

$$\sigma_c = \sigma_f V_f + \sigma_m (1 - V_f)$$

For our baseline E-glass/epoxy system:
- **E-Glass Fibre Tensile Strength ($\sigma_f$):** $3400.0\ \mathrm{MPa}$ (density $\rho_f = 2.58\ \mathrm{g/cm^3}$)
- **Epoxy Matrix Tensile Strength ($\sigma_m$):** $70.0\ \mathrm{MPa}$ (density $\rho_m = 1.18\ \mathrm{g/cm^3}$)

At our reference fibre volume fraction $V_f = 0.50$:

$$\sigma_{c,\text{ideal}} = (3400.0 \times 0.50) + (70.0 \times 0.50) = 1700.0 + 35.0 = 1735.0\ \mathrm{MPa}$$

The fibres carry $98.0\%$ of the axial tensile load, while the matrix carries only $2.0\%$.

### 2.2 Volume-to-Weight Fraction Conversion
Because manufacturing resin and fabric are measured by mass, conversion between volume fraction $V_f$ and weight fraction $W_f$ is governed by constituent densities:

$$W_f = \frac{V_f \rho_f}{V_f \rho_f + (1 - V_f) \rho_m}$$

At $V_f = 0.50$:

$$W_f = \frac{0.50 \times 2.58}{0.50 \times 2.58 + 0.50 \times 1.18} = \frac{1.29}{1.88} = 0.6862\ (68.6\% \approx 69\%)$$

Composite bulk density is $\rho_c = 1.88\ \mathrm{g/cm^3}$.

### 2.3 Why Measured Strength Falls Short
Four primary physical effects push physical composite strength below the idealized rule-of-mixtures prediction:
1. **Micro-Voids & Porosity:** Trapped volatiles reduce net load-bearing cross-section and create local stress concentrations ($K_t \approx 2 - 3$).
2. **Weak Fibre-Matrix Interfacial Bonding:** Incomplete sizing adhesion restricts shear-lag load transfer from matrix to broken fibre ends.
3. **Fibre Misalignment & Waviness:** Filament angular deviations ($\theta \approx 1^\circ - 3^\circ$) introduce off-axis shear coupling following Krenchel's $\cos^4\theta$ law.
4. **Manufacturing Variation & Weibull Flaw Dispersion:** Deviations in cure temperature and consolidation pressure alter resin crosslink density, while bundle flaw statistics reduce effective strand strength compared to single monofilaments.

---

## 3. Dataset Generation & Simulation Setup

To evaluate whether machine learning can accurately correct the classical formula, we developed a simulation pipeline modeling $600$ continuous unidirectional specimens:

```
[ Input Parameters ]
  • Fibre Volume Fraction: Vf in [0.30, 0.60]
  • Cure Temperature:      T in [80, 140] °C
  • Consolidation Pressure: P in [0.20, 1.00] MPa
  • Analytical Baseline:   RoM = 3400*Vf + 70*(1 - Vf)
             │
             ▼
[ Physical Degradation Model ]
  • Void reduction via pressure consolidation: P -> (1 - Vv)^2.5
  • Cure kinetics optimization: T_opt = 115 °C
  • Base Weibull bundle knockdown (~0.86)
             │
             ▼
[ Test Scatter Noise ]
  • 3% Gaussian experimental testing error
             │
             ▼
[ Final Target: Tensile Strength (MPa) ]
```

The 600 specimens are partitioned using an **80/20 train/test split with fixed random seed 42**:
- **Training Set:** $480$ specimens (used exclusively for model fitting and hyperparameter tuning)
- **Test Set:** $120$ specimens (held out and used solely for final scoring)

All data is stored in `data/synthetic_composite_dataset.csv`.

---

## 4. Machine Learning Model Formulations

Four predictive approaches are evaluated:

### 4.1 Model 1: Rule of Mixtures (Analytical Baseline, No ML)
Direct application of the textbook formula without statistical fitting:
$$\hat{y}_{\text{RoM}} = \sigma_f V_f + \sigma_m (1 - V_f)$$

### 4.2 Model 2: Linear Regression (Physics-Informed ML)
Fits an ordinary least squares regression plane utilizing all four inputs:
$$\hat{y}_{\text{LR}} = \beta_0 + \beta_1 V_f + \beta_2 T + \beta_3 P + \beta_4 \sigma_{c,\text{RoM}}$$

### 4.3 Model 3: Random Forest Regressor
An ensemble of $300$ de-correlated decision trees trained with bootstrap aggregation (bagging) and random feature sub-selection:
$$\hat{y}_{\text{RF}} = \frac{1}{300} \sum_{b=1}^{300} T_b(\mathbf{x})$$

### 4.4 Model 4: Gradient Boosting Regressor
An additive ensemble of sequential shallow regression trees that iteratively minimizes the squared-error loss function:
$$\hat{y}_{\text{GB}}^{(m)} = \hat{y}_{\text{GB}}^{(m-1)} + \gamma_m h_m(\mathbf{x})$$

---

## 5. Simulation Results & Discussion

Table 1 summarizes the performance of the analytical baseline and the three machine learning models evaluated on the held-out test set ($N = 120$).

### Table 1: Model Comparison on Synthetic Test Set (N = 120, Seed = 42)
| Model Name | $R^2$ Score | RMSE ($\mathrm{MPa}$) | MAE ($\mathrm{MPa}$) | Model Category | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Rule of Mixtures Alone** | **$-0.898$** | **$383.4$** | **$362.9$** | Analytical Baseline | Textbook formula (No ML) |
| **Linear Regression** | **$0.879$** | **$104.2$** | **$82.5$** | Physics-Informed ML | Fits linear correction plane |
| **Random Forest (300 trees)** | **$0.853$** | **$114.6$** | **$89.9$** | Ensemble ML | Bagged decision trees |
| **Gradient Boosting** | **$0.841$** | **$118.2$** | **$93.4$** | Boosting Ensemble | Sequential gradient trees |

### Key Observations:
1. **The Negative $R^2$ of Classical RoM:**  
   $R^2$ is defined as $1 - (SS_{\text{res}} / SS_{\text{tot}})$. Because the uncalibrated Rule of Mixtures exhibits a large positive bias (overestimating physical strength by $300 \text{ to } 400\ \mathrm{MPa}$), its sum of squared errors exceeds the natural variance of the test data, producing $R^2 = -0.898$.
2. **Close ML Performance Cluster:**  
   The three machine learning algorithms achieve $R^2$ scores clustered between **$0.84$ and $0.88$**. The differences between them are minor, indicating that the synthetic simulation does not strongly favor one algorithm over another.
3. **Linear Regression Strength:**  
   Linear Regression slightly outperforms the tree-based models ($R^2 = 0.879$ vs $0.853$ and $0.841$). Because the dominant physical relationship governing tensile strength is the linear volume fraction dependence ($\sigma_f V_f$), a linear plane captures the global trend cleanly without the localized step-function variance inherent in decision trees.
4. **Predicted vs. Actual Alignment:**  
   Scatter plots of predicted versus actual tensile strength across the test samples cluster tightly along the $1:1$ ideal identity line, confirming that machine learning successfully corrects for void and cure variations.

---

## 6. Limitations & Future Physical Validation

We explicitly emphasize the limitations of this study:
1. **Synthetic Data Nature:** All metrics ($R^2 = 0.84 - 0.88$) are derived from simulated data. While the simulation embodies physical void compaction and cure kinetics principles, it does not constitute physical empirical evidence.
2. **Constituent Datasheet Checks:** Handbook values for E-glass ($\sigma_f = 3400\ \mathrm{MPa}$) and epoxy ($\sigma_m = 70\ \mathrm{MPa}$) represent typical properties and must be confirmed against supplier lot certificates.
3. **Extrapolation Bounds:** Machine learning models trained on $V_f \in [0.30, 0.60]$ lose predictive reliability outside this window.

### Recommended Next Steps for Laboratory Validation:
- Fabricate unidirectional E-glass/epoxy coupons across $V_f \in [0.30, 0.40, 0.50, 0.60]$.
- Vary cure temperature at two levels ($100^\circ\mathrm{C}$ and $130^\circ\mathrm{C}$) and pressure at two levels ($0.3\ \mathrm{MPa}$ and $0.7\ \mathrm{MPa}$).
- Conduct uniaxial tensile testing in accordance with **ASTM D3039** (at least 5 replicate coupons per condition).
- Measure actual fibre volume fraction and void content via **ASTM D3171** matrix burn-off / resin digestion.
- Retrain the pipeline on the physical test matrix to establish true industrial predictive accuracy.

---

## 7. Conclusions & Engineering Recommendations

1. **Analytical Baseline Role:** The Rule of Mixtures provides a transparent, physics-based upper-bound baseline, but cannot be used alone for final structural sizing.
2. **Data-Driven Error Correction:** Combining the analytical Rule of Mixtures with processing variables enables machine learning models to capture void and cure kinetics effects with $84\% - 88\%$ explained variance.
3. **Early-Stage Screening Feasibility:** The hybrid physics-ML pipeline enables rapid, cost-effective screening of composite laminates during conceptual aerospace, automotive, and wind turbine design.
4. **Validation Prerequisite:** Physical laboratory validation on measured GFRP coupons remains mandatory before committing to safety-critical structural adoption.

---

## 8. Academic References

1. **Jones, R. M. (1999).** *Mechanics of Composite Materials*, 2nd Edition. Taylor & Francis / CRC Press. ISBN: 978-1560327127.
2. **Hull, D., & Clyne, T. W. (1996).** *An Introduction to Composite Materials*, 2nd Edition. Cambridge University Press. ISBN: 978-0521388559.
3. **Daniel, I. M., & Ishai, O. (2006).** *Engineering Mechanics of Composite Materials*, 2nd Edition. Oxford University Press. ISBN: 978-0195150971.
4. **Mallick, P. K. (2007).** *Fiber-Reinforced Composites: Materials, Manufacturing, and Design*, 3rd Edition. CRC Press. ISBN: 978-0849342059.
5. **ASTM D3039/D3039M-17 (2017).** *Standard Test Method for Tensile Properties of Polymer Matrix Composite Materials*. ASTM International, West Conshohocken, PA.
6. **ASTM D3171-15 (2016).** *Standard Test Methods for Constituent Content of Composite Materials*. ASTM International, West Conshohocken, PA.
7. **Soden, P. D., Hinton, M. J., & Kaddour, A. S. (1998).** "Lamina properties, lay-up configurations and loading conditions for a range of fibre-reinforced composite laminates." *Composites Science and Technology*, 58(7), 1011–1022.
8. **Krenchel, H. (1964).** *Fibre Reinforcement: Theoretical and Practical Investigations of the Elasticity and Strength of Fibre-Reinforced Materials*. Akademisk Forlag, Copenhagen.
9. **Weibull, W. (1951).** "A statistical distribution function of wide applicability." *Journal of Applied Mechanics*, 18(3), 293–297.
10. **Chamis, C. C. (1989).** "Mechanics of composite materials: Past, present, and a future." *Journal of Composites Technology and Research*, 11(1), 3–14.
