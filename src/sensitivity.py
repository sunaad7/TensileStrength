"""
TensileCheckmate: Sensitivity & Parametric Analysis Engine
Performs parametric sweeps, Tornado sensitivity analysis, and bounding envelope calculations.
"""

import numpy as np
import pandas as pd
from src.micromechanics import (
    ConstituentProperties,
    classical_rule_of_mixtures,
    modified_rule_of_mixtures,
    volume_to_weight_fraction
)


def run_parametric_vf_sweep(
    vf_min: float = 0.10,
    vf_max: float = 0.70,
    num_points: int = 61,
    props: ConstituentProperties = ConstituentProperties()
) -> pd.DataFrame:
    """
    Perform a sweep across fiber volume fractions and calculate:
    - Ideal Rule of Mixtures strength
    - Modified Rule of Mixtures strength
    - Fiber and matrix weight percentages
    - Composite density
    - Longitudinal modulus
    """
    vf_values = np.linspace(vf_min, vf_max, num_points)
    rows = []

    for vf in vf_values:
        wf_info = volume_to_weight_fraction(vf, props)
        sigma_ideal = classical_rule_of_mixtures(vf, props)
        mod_info = modified_rule_of_mixtures(vf, props=props)

        # Modulus
        E_1_GPa = (props.E_f * vf + props.E_m * (1.0 - vf)) / 1000.0

        rows.append({
            "V_f": round(vf, 4),
            "W_f": round(wf_info["W_f"], 4),
            "weight_percent_fiber": round(wf_info["weight_percent_fiber"], 2),
            "rho_c_g_cm3": round(wf_info["rho_c"], 3),
            "E_1_GPa": round(E_1_GPa, 2),
            "sigma_c_ideal_MPa": round(sigma_ideal, 2),
            "sigma_c_modified_MPa": round(mod_info["sigma_c_modified"], 2),
            "knockdown_gap_MPa": round(mod_info["knockdown_gap"], 2),
            "knockdown_pct": round(mod_info["knockdown_percentage"], 2),
            "fiber_load_contrib_MPa": round(mod_info["fiber_load_contribution"], 2),
            "matrix_load_contrib_MPa": round(mod_info["matrix_load_contribution"], 2),
        })

    return pd.DataFrame(rows)


def run_tornado_sensitivity(
    baseline_vf: float = 0.50,
    baseline_props: ConstituentProperties = ConstituentProperties(),
    variation_pct: float = 0.20
) -> pd.DataFrame:
    """
    Perform a One-At-a-Time (OAT) sensitivity analysis around the baseline case
    to determine which parameters have the highest impact on composite tensile strength.
    """
    base_res = modified_rule_of_mixtures(baseline_vf, props=baseline_props)
    base_strength = base_res["sigma_c_modified"]

    # Parameter variations: (Name, Param key, low_val, high_val, baseline_val, unit)
    params = [
        {
            "name": "Fiber Volume Fraction (V_f)",
            "unit": "-",
            "base": baseline_vf,
            "low": baseline_vf * (1.0 - variation_pct),
            "high": min(0.68, baseline_vf * (1.0 + variation_pct)),
            "calc_low": lambda v: modified_rule_of_mixtures(v, props=baseline_props)["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(v, props=baseline_props)["sigma_c_modified"]
        },
        {
            "name": "Fiber Tensile Strength (sigma_fu)",
            "unit": "MPa",
            "base": baseline_props.sigma_fu,
            "low": baseline_props.sigma_fu * (1.0 - variation_pct),
            "high": baseline_props.sigma_fu * (1.0 + variation_pct),
            "calc_low": lambda v: modified_rule_of_mixtures(baseline_vf, props=ConstituentProperties(sigma_fu=v))["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(baseline_vf, props=ConstituentProperties(sigma_fu=v))["sigma_c_modified"]
        },
        {
            "name": "Weibull Bundle Factor (eta_w)",
            "unit": "-",
            "base": 0.63,
            "low": 0.63 * (1.0 - variation_pct),
            "high": min(0.85, 0.63 * (1.0 + variation_pct)),
            "calc_low": lambda v: modified_rule_of_mixtures(baseline_vf, weibull_bundle_factor=v, props=baseline_props)["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(baseline_vf, weibull_bundle_factor=v, props=baseline_props)["sigma_c_modified"]
        },
        {
            "name": "Void Content (V_v)",
            "unit": "%",
            "base": 0.015,
            # For voids, higher void reduces strength (swapped low/high impact)
            "low": 0.005,  # 0.5% (fewer voids -> higher strength)
            "high": 0.035, # 3.5% (more voids -> lower strength)
            "calc_low": lambda v: modified_rule_of_mixtures(baseline_vf, void_content=v, props=baseline_props)["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(baseline_vf, void_content=v, props=baseline_props)["sigma_c_modified"]
        },
        {
            "name": "Fiber Misalignment Angle (theta)",
            "unit": "deg",
            "base": 2.0,
            "low": 0.5,    # Tight alignment
            "high": 5.0,   # Greater misalignment
            "calc_low": lambda v: modified_rule_of_mixtures(baseline_vf, misalignment_deg=v, props=baseline_props)["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(baseline_vf, misalignment_deg=v, props=baseline_props)["sigma_c_modified"]
        },
        {
            "name": "Matrix Tensile Strength (sigma_mu)",
            "unit": "MPa",
            "base": baseline_props.sigma_mu,
            "low": baseline_props.sigma_mu * (1.0 - variation_pct),
            "high": baseline_props.sigma_mu * (1.0 + variation_pct),
            "calc_low": lambda v: modified_rule_of_mixtures(baseline_vf, props=ConstituentProperties(sigma_mu=v))["sigma_c_modified"],
            "calc_high": lambda v: modified_rule_of_mixtures(baseline_vf, props=ConstituentProperties(sigma_mu=v))["sigma_c_modified"]
        }
    ]

    results = []
    for p in params:
        str_low = p["calc_low"](p["low"])
        str_high = p["calc_high"](p["high"])

        # Determine min and max strength from low/high parameter inputs
        min_str = min(str_low, str_high)
        max_str = max(str_low, str_high)
        swing = max_str - min_str

        results.append({
            "parameter": p["name"],
            "base_value": p["base"],
            "low_param": p["low"],
            "high_param": p["high"],
            "strength_at_low_param": round(str_low, 2),
            "strength_at_high_param": round(str_high, 2),
            "delta_negative": round(min_str - base_strength, 2),
            "delta_positive": round(max_str - base_strength, 2),
            "total_swing_MPa": round(swing, 2),
            "impact_percentage": round((swing / base_strength) * 100.0, 2)
        })

    df = pd.DataFrame(results)
    # Sort descending by total swing
    df = df.sort_values(by="total_swing_MPa", ascending=False).reset_index(drop=True)
    return df
