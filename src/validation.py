"""
TensileCheckmate: Model Validation & Experimental Benchmarking Engine
Compares Classical and Modified RoM against published experimental literature data.
"""

import pandas as pd
import numpy as np
from src.micromechanics import (
    ConstituentProperties,
    classical_rule_of_mixtures,
    modified_rule_of_mixtures
)


def load_experimental_data(filepath: str = "data/published_experimental_data.csv") -> pd.DataFrame:
    """Load the published experimental benchmark dataset."""
    df = pd.read_csv(filepath)
    return df


def evaluate_models_against_benchmark(
    df_exp: pd.DataFrame = None,
    props: ConstituentProperties = ConstituentProperties()
) -> dict:
    """
    Calculate predictions of Classical RoM and Modified RoM for each experimental specimen,
    and evaluate statistical metrics (MAE, RMSE, MAPE, R^2).
    """
    if df_exp is None:
        df_exp = load_experimental_data()

    y_actual = df_exp["Tensile_Strength_MPa"].values
    vf_values = df_exp["Fiber_Volume_Fraction"].values
    void_values = (df_exp["Void_Content_Percent"].values) / 100.0

    y_pred_classical = []
    y_pred_modified = []

    for vf, void in zip(vf_values, void_values):
        # Classical RoM (only depends on Vf)
        sig_c = classical_rule_of_mixtures(vf, props)
        y_pred_classical.append(sig_c)

        # Modified RoM (uses reported void content or default 1.5% and 2 deg misalignment)
        v_void = void if not np.isnan(void) and void > 0 else 0.015
        mod_res = modified_rule_of_mixtures(
            vf,
            void_content=v_void,
            misalignment_deg=2.0,
            weibull_bundle_factor=0.63,
            interface_efficiency=0.95,
            props=props
        )
        y_pred_modified.append(mod_res["sigma_c_modified"])

    y_pred_classical = np.array(y_pred_classical)
    y_pred_modified = np.array(y_pred_modified)

    def calc_metrics(y_true, y_pred):
        residuals = y_true - y_pred
        mae = np.mean(np.abs(residuals))
        rmse = np.sqrt(np.mean(residuals ** 2))
        mape = np.mean(np.abs(residuals / y_true)) * 100.0

        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        return {
            "MAE_MPa": round(mae, 2),
            "RMSE_MPa": round(rmse, 2),
            "MAPE_pct": round(mape, 2),
            "R2": round(r2, 4),
            "mean_bias_MPa": round(np.mean(y_pred - y_true), 2)
        }

    metrics_classical = calc_metrics(y_actual, y_pred_classical)
    metrics_modified = calc_metrics(y_actual, y_pred_modified)

    df_results = df_exp.copy()
    df_results["Classical_RoM_MPa"] = np.round(y_pred_classical, 1)
    df_results["Modified_RoM_MPa"] = np.round(y_pred_modified, 1)
    df_results["Error_Classical_MPa"] = np.round(y_pred_classical - y_actual, 1)
    df_results["Error_Modified_MPa"] = np.round(y_pred_modified - y_actual, 1)
    df_results["Pct_Error_Classical"] = np.round(((y_pred_classical - y_actual) / y_actual) * 100.0, 1)
    df_results["Pct_Error_Modified"] = np.round(((y_pred_modified - y_actual) / y_actual) * 100.0, 1)

    return {
        "df_comparison": df_results,
        "metrics_classical": metrics_classical,
        "metrics_modified": metrics_modified
    }
