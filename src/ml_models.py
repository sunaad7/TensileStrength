"""
TensileCheckmate: Machine Learning & Simulation Pipeline
Simulates 600 GFRP specimens combining the Rule of Mixtures with manufacturing effects
and fits Linear Regression, Random Forest (300 trees), and Gradient Boosting.
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def generate_synthetic_dataset(
    n_samples: int = 600,
    random_seed: int = 42,
    output_path: str = "data/synthetic_composite_dataset.csv"
) -> pd.DataFrame:
    """
    Generate 600 simulated E-glass/epoxy specimens:
    Inputs:
      - Fiber volume fraction (Vf): 0.30 to 0.60
      - Cure temperature (T_cure): 80 to 140 deg C
      - Consolidation pressure (P): 0.2 to 1.0 MPa
      - Rule-of-mixtures estimate (RoM): sigma_f * Vf + sigma_m * (1 - Vf)
    Target:
      - Tensile strength (reduced by imperfect bonding and voids, plus 3% test scatter)
    """
    np.random.seed(random_seed)

    # Input distributions
    Vf = np.random.uniform(0.30, 0.60, n_samples)
    T = np.random.uniform(80.0, 140.0, n_samples)
    P = np.random.uniform(0.20, 1.00, n_samples)

    # Constituent handbook properties
    sigma_f = 3400.0  # E-glass monofilament (MPa)
    sigma_m = 70.0    # Epoxy matrix (MPa)

    # Rule of mixtures estimate (Physics baseline)
    RoM = sigma_f * Vf + sigma_m * (1.0 - Vf)

    # Physical degradation simulation:
    # 1. Base bonding and Weibull bundle factor (~0.86)
    # 2. Consolidation pressure effect (P: 0.2 to 1.0 MPa, void reduction)
    # 3. Cure temperature kinetics (T: 80 to 140 C, optimal near 110-120 C)
    # 4. Experimental scatter (~3%)
    k1 = 0.862
    offset = 173.0
    temp_effect = 22.0 * np.sin((T - 80.0) / 60.0 * np.pi)
    press_effect = 18.0 * (P - 0.60)
    
    strength_clean = k1 * RoM - offset + temp_effect + press_effect
    noise = np.random.normal(0, 98.0, n_samples)
    tensile_strength = np.round(strength_clean + noise, 2)

    df = pd.DataFrame({
        "Specimen_ID": [f"GFRP-SYN-{i+1:04d}" for i in range(n_samples)],
        "Fiber_Volume_Fraction": np.round(Vf, 4),
        "Cure_Temperature_C": np.round(T, 1),
        "Pressure_MPa": np.round(P, 3),
        "Rule_of_Mixtures_MPa": np.round(RoM, 2),
        "Tensile_Strength_MPa": tensile_strength
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {n_samples} simulated samples -> {output_path}")
    return df


def train_and_evaluate_models(dataset_path: str = "data/synthetic_composite_dataset.csv"):
    """
    Train Linear Regression, Random Forest (300 trees), and Gradient Boosting
    on 80% training data (480 samples) and evaluate on 20% test data (120 samples).
    """
    if not os.path.exists(dataset_path):
        df = generate_synthetic_dataset(output_path=dataset_path)
    else:
        df = pd.read_csv(dataset_path)

    features = ["Fiber_Volume_Fraction", "Cure_Temperature_C", "Pressure_MPa", "Rule_of_Mixtures_MPa"]
    X = df[features].values
    y = df["Tensile_Strength_MPa"].values
    rom = df["Rule_of_Mixtures_MPa"].values

    # 80/20 train/test split with fixed random seed 42
    X_train, X_test, y_train, y_test, rom_train, rom_test = train_test_split(
        X, y, rom, test_size=0.20, random_state=42
    )

    # 1. Rule of Mixtures Baseline (No ML)
    mae_rom = mean_absolute_error(y_test, rom_test)
    rmse_rom = np.sqrt(mean_squared_error(y_test, rom_test))
    r2_rom = r2_score(y_test, rom_test)

    # 2. Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    r2_lr = r2_score(y_test, y_pred_lr)

    # 3. Random Forest (300 trees, random seed 42)
    rf = RandomForestRegressor(n_estimators=300, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)

    # 4. Gradient Boosting (random seed 42)
    gb = GradientBoostingRegressor(random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    mae_gb = mean_absolute_error(y_test, y_pred_gb)
    rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))
    r2_gb = r2_score(y_test, y_pred_gb)

    results_table = pd.DataFrame([
        {
            "Model": "Rule of Mixtures (Physics Baseline)",
            "R2": round(r2_rom, 3),
            "RMSE_MPa": round(rmse_rom, 1),
            "MAE_MPa": round(mae_rom, 1),
            "Type": "Analytical Baseline (No ML)"
        },
        {
            "Model": "Linear Regression",
            "R2": round(r2_lr, 3),
            "RMSE_MPa": round(rmse_lr, 1),
            "MAE_MPa": round(mae_lr, 1),
            "Type": "Physics-Informed ML"
        },
        {
            "Model": "Random Forest (300 trees)",
            "R2": round(r2_rf, 3),
            "RMSE_MPa": round(rmse_rf, 1),
            "MAE_MPa": round(mae_rf, 1),
            "Type": "Ensemble ML"
        },
        {
            "Model": "Gradient Boosting",
            "R2": round(r2_gb, 3),
            "RMSE_MPa": round(rmse_gb, 1),
            "MAE_MPa": round(mae_gb, 1),
            "Type": "Ensemble ML"
        }
    ])

    return {
        "df_all": df,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "rom_test": rom_test,
        "models": {
            "lr": lr,
            "rf": rf,
            "gb": gb
        },
        "predictions": {
            "rom": rom_test,
            "lr": y_pred_lr,
            "rf": y_pred_rf,
            "gb": y_pred_gb
        },
        "metrics_table": results_table
    }


if __name__ == "__main__":
    generate_synthetic_dataset()
    res = train_and_evaluate_models()
    print("\n--- Model Evaluation on Synthetic Test Data (120 Samples) ---")
    print(res["metrics_table"].to_string(index=False))
