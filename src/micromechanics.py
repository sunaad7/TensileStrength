"""
TensileCheckmate: Composite Micromechanics Engine
Calculates Classical and Modified Rule of Mixtures for Unidirectional GFRP.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class ConstituentProperties:
    """Properties of composite constituents."""
    # E-Glass Fiber
    rho_f: float = 2.58       # Density (g/cm^3)
    sigma_fu: float = 3400.0  # Pristine monofilament ultimate tensile strength (MPa)
    E_f: float = 72400.0      # Young's modulus (MPa)
    epsilon_fu: float = 0.028 # Failure strain (mm/mm)
    diameter_f: float = 15.0  # Fiber diameter (microns)

    # Epoxy Matrix (DGEBA / Amine cured)
    rho_m: float = 1.18       # Density (g/cm^3)
    sigma_mu: float = 70.0    # Ultimate tensile strength (MPa)
    E_m: float = 3400.0       # Young's modulus (MPa)
    epsilon_mu: float = 0.040 # Failure strain (mm/mm)


def volume_to_weight_fraction(V_f: float, props: ConstituentProperties = ConstituentProperties()) -> dict:
    """
    Convert fiber volume fraction (V_f) to fiber weight fraction (W_f) and composite density.
    Formula: W_f = (V_f * rho_f) / (V_f * rho_f + (1 - V_f) * rho_m)
    """
    if not (0.0 <= V_f <= 1.0):
        raise ValueError(f"Fiber volume fraction V_f must be between 0.0 and 1.0, got {V_f}")
    rho_c = V_f * props.rho_f + (1.0 - V_f) * props.rho_m
    W_f = (V_f * props.rho_f) / rho_c
    W_m = 1.0 - W_f
    return {
        "V_f": V_f,
        "V_m": 1.0 - V_f,
        "W_f": W_f,
        "W_m": W_m,
        "rho_c": rho_c,
        "weight_percent_fiber": W_f * 100.0,
        "weight_percent_matrix": W_m * 100.0,
    }


def classical_rule_of_mixtures(
    V_f: float,
    props: ConstituentProperties = ConstituentProperties(),
    strain_compatible: bool = False
) -> float:
    """
    Classical Voigt Rule of Mixtures for longitudinal tensile strength:
    - Standard handbook form: sigma_c = sigma_fu * V_f + sigma_mu * (1 - V_f)
    - Strain-compatible form: sigma_c = sigma_fu * V_f + (E_m * epsilon_fu) * (1 - V_f)
    """
    if not (0.0 <= V_f <= 1.0):
        raise ValueError(f"Fiber volume fraction V_f must be between 0.0 and 1.0, got {V_f}")
    V_m = 1.0 - V_f
    if strain_compatible:
        sigma_m_effective = min(props.sigma_mu, props.E_m * props.epsilon_fu)
        return props.sigma_fu * V_f + sigma_m_effective * V_m
    else:
        return props.sigma_fu * V_f + props.sigma_mu * V_m


def modified_rule_of_mixtures(
    V_f: float,
    void_content: float = 0.015,     # 1.5% voids
    misalignment_deg: float = 2.0,   # 2 degrees average misalignment
    weibull_bundle_factor: float = 0.63, # Weibull gauge length & bundle load-sharing knockdown (~0.63)
    interface_efficiency: float = 0.95,  # Silane sizing bond quality
    props: ConstituentProperties = ConstituentProperties()
) -> dict:
    """
    Modified Rule of Mixtures accounting for physical knockdown mechanisms:
    sigma_c_real = (eta_theta * eta_v * eta_w * eta_int) * sigma_fu * V_f + sigma_m' * (1 - V_f)

    Where:
    - eta_theta = cos^4(theta): Krenchel fiber orientation factor
    - eta_v = (1 - void_content)^3.0: Void stress concentration knockdown
    - eta_w: Weibull fiber bundle statistical knockdown (monofilament vs bundle)
    - eta_int: Fiber-matrix interface bond efficiency
    """
    if not (0.0 <= V_f <= 1.0):
        raise ValueError(f"Fiber volume fraction V_f must be between 0.0 and 1.0, got {V_f}")
    if not (0.0 <= void_content <= 1.0):
        raise ValueError(f"Void content must be between 0.0 and 1.0, got {void_content}")
    theta_rad = np.radians(misalignment_deg)
    eta_theta = np.cos(theta_rad) ** 4
    eta_v = (1.0 - void_content) ** 3.0
    eta_w = weibull_bundle_factor
    eta_int = interface_efficiency

    # Combined fiber efficiency factor
    eta_fiber_total = eta_theta * eta_v * eta_w * eta_int

    # Matrix stress at composite failure strain
    sigma_m_effective = min(props.sigma_mu, props.E_m * props.epsilon_fu)
    V_m = 1.0 - V_f

    sigma_c_ideal = classical_rule_of_mixtures(V_f, props, strain_compatible=False)
    sigma_c_modified = (eta_fiber_total * props.sigma_fu * V_f) + (sigma_m_effective * V_m)

    knockdown_gap = sigma_c_ideal - sigma_c_modified
    knockdown_percentage = (knockdown_gap / sigma_c_ideal) * 100.0

    return {
        "V_f": V_f,
        "sigma_c_ideal": sigma_c_ideal,
        "sigma_c_modified": sigma_c_modified,
        "knockdown_gap": knockdown_gap,
        "knockdown_percentage": knockdown_percentage,
        "eta_theta": eta_theta,
        "eta_v": eta_v,
        "eta_w": eta_w,
        "eta_int": eta_int,
        "eta_fiber_total": eta_fiber_total,
        "fiber_load_contribution": (eta_fiber_total * props.sigma_fu * V_f),
        "matrix_load_contribution": (sigma_m_effective * V_m),
    }


def composite_elastic_moduli(V_f: float, props: ConstituentProperties = ConstituentProperties()) -> dict:
    """
    Calculate longitudinal and transverse moduli:
    - E_1 (Longitudinal): Voigt parallel model: E_1 = E_f * V_f + E_m * (1 - V_f)
    - E_2 (Transverse): Halpin-Tsai semi-empirical model (xi = 2 for circular fibers)
    """
    if not (0.0 <= V_f <= 1.0):
        raise ValueError(f"Fiber volume fraction V_f must be between 0.0 and 1.0, got {V_f}")
    V_m = 1.0 - V_f
    E_1 = props.E_f * V_f + props.E_m * V_m

    # Halpin-Tsai for E_2
    xi = 2.0  # Reinforcement geometry parameter for square/hex array circular fibers
    eta_HT = ((props.E_f / props.E_m) - 1.0) / ((props.E_f / props.E_m) + xi)
    E_2 = props.E_m * (1.0 + xi * eta_HT * V_f) / (1.0 - eta_HT * V_f)

    # Major Poisson's ratio
    nu_f = 0.22
    nu_m = 0.35
    nu_12 = nu_f * V_f + nu_m * V_m

    return {
        "E_1_MPa": E_1,
        "E_1_GPa": E_1 / 1000.0,
        "E_2_MPa": E_2,
        "E_2_GPa": E_2 / 1000.0,
        "nu_12": nu_12
    }


def generate_stress_strain_data(
    V_f: float = 0.50,
    props: ConstituentProperties = ConstituentProperties(),
    num_points: int = 200
) -> dict:
    """
    Generate synthetic stress-strain curves for E-Glass, Epoxy Matrix, and GFRP Lamina
    demonstrating linear elastic behavior and brittle catastrophic fracture.
    """
    # Strains up to failure
    eps_fiber = np.linspace(0, props.epsilon_fu, num_points)
    stress_fiber = props.E_f * eps_fiber

    # Epoxy matrix: slight softening/non-linearity before failure
    eps_matrix = np.linspace(0, props.epsilon_mu, num_points)
    # Secant or Ramberg-Osgood style matrix stress curve
    stress_matrix = props.E_m * eps_matrix * (1.0 - 0.25 * (eps_matrix / props.epsilon_mu))

    # Composite: linear up to fiber failure strain
    E_1 = props.E_f * V_f + props.E_m * (1.0 - V_f)
    eps_composite = np.linspace(0, props.epsilon_fu, num_points)

    # Composite stress according to Modified RoM at failure
    mod_result = modified_rule_of_mixtures(V_f, props=props)
    sigma_max = mod_result["sigma_c_modified"]
    stress_composite = (sigma_max / props.epsilon_fu) * eps_composite

    # Append post-failure brittle drop to zero
    eps_fiber_post = np.array([props.epsilon_fu, props.epsilon_fu * 1.05])
    stress_fiber_post = np.array([props.sigma_fu, 0.0])

    eps_comp_post = np.array([props.epsilon_fu, props.epsilon_fu * 1.05])
    stress_comp_post = np.array([sigma_max, 0.0])

    return {
        "fiber": {
            "strain_pct": np.concatenate([eps_fiber, eps_fiber_post]) * 100.0,
            "stress_MPa": np.concatenate([stress_fiber, stress_fiber_post])
        },
        "matrix": {
            "strain_pct": eps_matrix * 100.0,
            "stress_MPa": stress_matrix
        },
        "composite": {
            "strain_pct": np.concatenate([eps_composite, eps_comp_post]) * 100.0,
            "stress_MPa": np.concatenate([stress_composite, stress_comp_post])
        },
        "peak_stress_MPa": sigma_max,
        "failure_strain_pct": props.epsilon_fu * 100.0
    }
