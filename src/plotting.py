"""
TensileCheckmate: Figure Generation Suite
Produces publication-quality academic figures in Times New Roman with #0070C0 accents.
"""

import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from src.micromechanics import (
    ConstituentProperties,
    classical_rule_of_mixtures,
    modified_rule_of_mixtures,
    generate_stress_strain_data
)
from src.sensitivity import run_parametric_vf_sweep, run_tornado_sensitivity
from src.validation import evaluate_models_against_benchmark


# Configure global academic plotting style
def apply_academic_style():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'Georgia'],
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'lines.linewidth': 2.0,
        'axes.grid': True,
        'grid.alpha': 0.35,
        'grid.linestyle': '--',
        'axes.edgecolor': '#333333',
        'axes.linewidth': 1.0,
    })


PRIMARY_BLUE = '#0070C0'
DARK_BLUE = '#003366'
ACCENT_GRAY = '#666666'
LIGHT_GRAY = '#F2F4F7'
ACCENT_RED = '#C00000'
ACCENT_GREEN = '#008040'


def plot_fig1_rom_strength_curve(output_path: str = "figures/fig1_rom_strength_curve.png"):
    """
    Fig 1: Ideal Rule of Mixtures Tensile Strength vs Fiber Volume Fraction (Vf)
    Shows total composite strength with constituent contribution bands and key milestones.
    """
    apply_academic_style()
    df = run_parametric_vf_sweep(vf_min=0.0, vf_max=0.70, num_points=100)

    fig, ax = plt.subplots(figsize=(8, 5.2))

    # Stacked area for constituent contribution
    ax.fill_between(df["V_f"], 0, df["fiber_load_contrib_MPa"], color=PRIMARY_BLUE, alpha=0.25, label='Fiber Phase Contribution')
    ax.fill_between(df["V_f"], df["fiber_load_contrib_MPa"], df["sigma_c_ideal_MPa"], color='#8FAADC', alpha=0.35, label='Matrix Phase Contribution')

    # Ideal curve line
    ax.plot(df["V_f"], df["sigma_c_ideal_MPa"], color=PRIMARY_BLUE, linewidth=2.8, label=r'Ideal RoM: $\sigma_c = \sigma_f V_f + \sigma_m (1 - V_f)$')

    # Key highlight points mentioned in the presentation
    key_points = [
        (0.10, 403, "Vf = 0.10: 403 MPa"),
        (0.30, 1069, "Vf = 0.30: 1069 MPa"),
        (0.50, 1735, "Vf = 0.50 (Ref): 1735 MPa"),
        (0.60, 2068, "Vf = 0.60: 2068 MPa")
    ]

    for vf, val, lbl in key_points:
        ax.plot(vf, val, marker='o', markersize=7, color=DARK_BLUE)
        ax.annotate(lbl, (vf, val), textcoords="offset points", xytext=(-25, 12),
                    fontsize=9, weight='bold', color=DARK_BLUE,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=PRIMARY_BLUE, lw=1))

    # Reference case vertical line
    ax.axvline(0.50, color=ACCENT_GRAY, linestyle=':', alpha=0.7)

    ax.set_title('Ideal Tensile Strength of Unidirectional GFRP vs. Fiber Volume Fraction', pad=12)
    ax.set_xlabel('Fiber Volume Fraction ($V_f$)')
    ax.set_ylabel(r'Ideal Composite Tensile Strength $\sigma_c$ (MPa)')
    ax.set_xlim(0.0, 0.70)
    ax.set_ylim(0, 2500)
    ax.legend(loc='upper left', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig2_microstructure_schematic(output_path: str = "figures/fig2_microstructure_schematic.png"):
    """
    Fig 2: Unidirectional Ply Structure (Schematic Cross-Section at Vf = 0.50)
    Shows circular E-glass fibers in an epoxy matrix with clear legend and scale.
    """
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Matrix background rectangle
    rect = patches.Rectangle((0, 0), 10, 7.5, linewidth=2, edgecolor='#333333', facecolor='#E9ECF2')
    ax.add_patch(rect)

    # Place fibers in a regular hexagonal/staggered array (Vf ~ 0.50)
    r = 0.52  # Fiber radius in diagram units (~15 microns physical)
    dx = 1.45
    dy = 1.25

    fibers = []
    for row, y in enumerate(np.arange(0.8, 7.0, dy)):
        offset = (dx / 2.0) if (row % 2 == 1) else 0.0
        for x in np.arange(0.8 + offset, 9.5, dx):
            c = patches.Circle((x, y), r, edgecolor=PRIMARY_BLUE, facecolor='#BDD7EE', linewidth=1.8)
            ax.add_patch(c)
            fibers.append((x, y))

    # Add a few small voids to demonstrate real microstructure
    voids = [(3.2, 3.8), (6.8, 2.1), (5.1, 5.5)]
    for vx, vy in voids:
        v_patch = patches.Ellipse((vx, vy), 0.28, 0.18, angle=15, edgecolor='#555555', facecolor='#2B2B2B', linewidth=1.2)
        ax.add_patch(v_patch)

    # Fiber diameter dimension indicator
    fx, fy = fibers[7]
    ax.annotate('', xy=(fx - r, fy), xytext=(fx + r, fy),
                arrowprops=dict(arrowstyle='<->', color='#C00000', lw=1.5))
    ax.text(fx, fy + 0.65, r'Fiber Dia $\approx 15\ \mu\mathrm{m}$', color='#C00000',
            fontsize=9.5, weight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec='#C00000', lw=0.8))

    # Axis annotation (fibers running into page, load along fiber length)
    ax.text(5.0, 7.0, 'Unidirectional Ply Transverse Cross-Section ($V_f \\approx 0.50$)',
            fontsize=12, weight='bold', color=DARK_BLUE, ha='center')
    ax.text(5.0, 0.35, r'$\odot$ Fiber Axis: Longitudinal direction ($x_1$) is normal to the page (tensile loading axis)',
            fontsize=9.5, color='#333333', ha='center', style='italic')

    # Custom Legend
    legend_elements = [
        patches.Patch(facecolor='#BDD7EE', edgecolor=PRIMARY_BLUE, linewidth=1.8, label=r'E-Glass Fibers ($\sigma_f = 3400\ \mathrm{MPa},\ E_f = 72.4\ \mathrm{GPa}$)'),
        patches.Patch(facecolor='#E9ECF2', edgecolor='#333333', linewidth=1.5, label=r'Epoxy Matrix ($\sigma_m = 70\ \mathrm{MPa},\ E_m = 3.4\ \mathrm{GPa}$)'),
        patches.Patch(facecolor='#2B2B2B', edgecolor='#555555', linewidth=1.2, label=r'Micro-voids / Porosity (Defects: $\sim 1\text{--}2\%$)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, framealpha=0.95, edgecolor='#AAAAAA')

    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(-0.2, 7.7)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig3_stress_strain_schematic(output_path: str = "figures/fig3_stress_strain_schematic.png"):
    """
    Fig 3: Tensile Behaviour of GFRP (Schematic Stress-Strain Curve)
    Shows qualitative linear elastic behavior, constituent stiffness differences, and brittle fracture.
    No numerical axes as requested, clearly marked as schematic.
    """
    apply_academic_style()
    data = generate_stress_strain_data(V_f=0.50)

    fig, ax = plt.subplots(figsize=(8, 5.2))

    # Plot normalized/qualitative curves
    ax.plot(data["fiber"]["strain_pct"], data["fiber"]["stress_MPa"],
            color='#1F4E79', linewidth=2.5, label=r'E-Glass Monofilament (High $E$, High $\sigma_{fu}$, Brittle)')

    ax.plot(data["composite"]["strain_pct"], data["composite"]["stress_MPa"],
            color=PRIMARY_BLUE, linewidth=3.0, label='UD GFRP Lamina (Longitudinal Tensile Response)')

    ax.plot(data["matrix"]["strain_pct"], data["matrix"]["stress_MPa"] * 10.0,  # Scaled for visibility
            color='#ED7D31', linewidth=2.2, linestyle='--',
            label=r'Epoxy Matrix ($10\times$ stress scale for visual comparison)')

    # Mark Peak Stress and Brittle Fracture
    peak_x = data["failure_strain_pct"]
    peak_y = data["peak_stress_MPa"]

    ax.plot(peak_x, peak_y, marker='*', markersize=14, color=ACCENT_RED)
    ax.annotate('Peak Tensile Strength ($X_t$)\n(Catastrophic Brittle Failure)',
                xy=(peak_x, peak_y), xytext=(peak_x - 1.2, peak_y + 120),
                arrowprops=dict(facecolor=ACCENT_RED, edgecolor=ACCENT_RED, arrowstyle='->', lw=1.8),
                fontsize=10, weight='bold', color=ACCENT_RED,
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFF0F0", ec=ACCENT_RED, lw=1))

    # Linear elastic region callout
    ax.annotate(r'Linear Elastic Region' + '\n' + r'($\sigma = E_1 \cdot \epsilon$)',
                xy=(1.0, 480), xytext=(0.4, 850),
                arrowprops=dict(facecolor=DARK_BLUE, edgecolor=DARK_BLUE, arrowstyle='->', lw=1.4),
                fontsize=9.5, color=DARK_BLUE, weight='bold')

    # Watermark / Banner noting schematic nature
    ax.text(0.5, 0.93, '[ SCHEMATIC REPRESENTATION — QUALITATIVE CONSTITUENT BEHAVIOR ]',
            transform=ax.transAxes, ha='center', fontsize=9.5, color='#888888',
            bbox=dict(boxstyle="square,pad=0.3", fc="#FAFAFA", ec="#DDDDDD", lw=0.8))

    ax.set_title('Schematic Tensile Stress–Strain Response of GFRP Composite and Constituents', pad=14)
    ax.set_xlabel(r'Tensile Strain ($\epsilon$) $\longrightarrow$ [No Plastic Yielding]')
    ax.set_ylabel(r'Tensile Stress ($\sigma$) $\longrightarrow$ [Brittle Rupture at Peak]')

    # Hide tick labels for pure schematic look
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(0, 3.8)
    ax.set_ylim(0, 3800)

    ax.legend(loc='center left', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig4_knockdown_mechanisms(output_path: str = "figures/fig4_knockdown_mechanisms.png"):
    """
    Fig 4: Why Measured Strength Falls Short (Decomposition of 4 Knockdown Mechanisms)
    Block diagram illustrating the transition from Ideal RoM (1735 MPa) to Measured (~1100 MPa).
    """
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(9.2, 5.6))

    # Top block: Ideal Rule of Mixtures
    box_ideal = patches.FancyBboxPatch((0.5, 4.0), 3.0, 1.2, boxstyle="round,pad=0.2",
                                      fc='#D9E1F2', ec=PRIMARY_BLUE, lw=2.2)
    ax.add_patch(box_ideal)
    ax.text(2.0, 4.8, r'Ideal Rule of Mixtures' + '\n' + r'$\sigma_c = \sigma_f V_f + \sigma_m (1 - V_f)$',
            ha='center', va='center', fontsize=11, weight='bold', color=DARK_BLUE)
    ax.text(2.0, 4.25, r'Baseline at $V_f = 0.50$: $\mathbf{1735\ \mathrm{MPa}}$',
            ha='center', va='center', fontsize=10, weight='bold', color=PRIMARY_BLUE)

    # 4 Knockdown Mechanism Blocks
    mechanisms = [
        ("1. Micro-Voids & Porosity",
         "• Trapped air / volatile gases\n• Stress concentration at void edges\n• Initiates premature micro-cracks",
         "#FCE4D6", "#C65911", 5.2, 4.2),
        ("2. Weak Interfacial Bonding",
         "• Incomplete chemical sizing adhesion\n• Shear-lag ineffective transfer length\n• Fiber-matrix debonding before break",
         "#FFF2CC", "#BF8F00", 5.2, 2.8),
        ("3. Fiber Misalignment & Waviness",
         r"• Out-of-plane & in-plane waviness" + "\n" + r"• Krenchel factor: $\eta_\theta = \cos^4(\theta)$" + "\n" + r"• Off-axis shear stress coupling",
         "#E2EFDA", "#375623", 5.2, 1.4),
        ("4. Weibull Flaw Dispersion",
         r"• Bundle statistical size effect" + "\n" + r"• Fiber strength scatter ($\sim 20\text{--}25\%$)" + "\n" + r"• Non-uniform cure residual stresses",
         "#F2DCDB", "#C00000", 5.2, 0.0)
    ]

    for title, desc, fc, ec, bx, by in mechanisms:
        box = patches.FancyBboxPatch((bx, by), 3.6, 1.15, boxstyle="round,pad=0.15",
                                     fc=fc, ec=ec, lw=1.6)
        ax.add_patch(box)
        ax.text(bx + 0.15, by + 0.9, title, fontsize=9.5, weight='bold', color=ec)
        ax.text(bx + 0.15, by + 0.42, desc, fontsize=7.8, color='#333333', va='center')

        # Arrows pointing from Ideal to mechanisms
        ax.annotate('', xy=(bx, by + 0.58), xytext=(3.65, 4.6),
                    arrowprops=dict(arrowstyle='->', color='#777777', lw=1.2, connectionstyle="angle3,angleA=0,angleB=-90"))

        # Arrows pointing from mechanisms to Real Measured
        ax.annotate('', xy=(9.2, 2.7), xytext=(bx + 3.75, by + 0.58),
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1.3, connectionstyle="angle3,angleA=0,angleB=90"))

    # Bottom Right: Measured / Modified Strength Box
    box_real = patches.FancyBboxPatch((9.2, 2.0), 3.1, 1.5, boxstyle="round,pad=0.2",
                                     fc='#E2EFDA', ec='#375623', lw=2.4)
    ax.add_patch(box_real)
    ax.text(10.75, 3.05, 'Real Measured GFRP Strength\n(ASTM D3039 Tests)',
            ha='center', va='center', fontsize=11, weight='bold', color='#276A3C')
    ax.text(10.75, 2.45, r'Observed: $\mathbf{1020\ \text{--}\ 1180\ \mathrm{MPa}}$',
            ha='center', va='center', fontsize=10.5, weight='bold', color='#1E4620')
    ax.text(10.75, 2.15, r'Knockdown: $\sim 30\%\ \text{to}\ 40\%$ below ideal',
            ha='center', va='center', fontsize=8.5, color='#444444', style='italic')

    # Title
    ax.text(6.3, 5.7, 'Micromechanical Knockdown Mechanisms: Why Measured Tensile Strength Falls Short',
            ha='center', fontsize=12.5, weight='bold', color=DARK_BLUE)

    ax.set_xlim(0.2, 12.6)
    ax.set_ylim(-0.3, 6.0)
    ax.axis('off')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig5_sensitivity_tornado(output_path: str = "figures/fig5_sensitivity_tornado.png"):
    """
    Fig 5: Parametric Sensitivity Analysis (Tornado Chart)
    Quantifies the influence of each microstructural variable on composite tensile strength.
    """
    apply_academic_style()
    df_tornado = run_tornado_sensitivity(baseline_vf=0.50, variation_pct=0.20)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))

    y_pos = np.arange(len(df_tornado))
    params = df_tornado["parameter"].tolist()
    delta_neg = df_tornado["delta_negative"].values
    delta_pos = df_tornado["delta_positive"].values

    # Plot horizontal tornado bars
    ax.barh(y_pos, delta_neg, height=0.55, align='center', color='#ED7D31', label='-20% Parameter Change (or adverse defect)')
    ax.barh(y_pos, delta_pos, height=0.55, align='center', color=PRIMARY_BLUE, label='+20% Parameter Change (or improved quality)')

    # Add data labels
    for i in range(len(params)):
        # Negative label
        ax.text(delta_neg[i] - 12, i, f"{delta_neg[i]:.0f} MPa", ha='right', va='center', fontsize=8.5, weight='bold', color='#A64000')
        # Positive label
        ax.text(delta_pos[i] + 12, i, f"+{delta_pos[i]:.0f} MPa", ha='left', va='center', fontsize=8.5, weight='bold', color=DARK_BLUE)

    ax.axvline(0, color='#333333', linewidth=1.2, linestyle='-')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params)
    ax.invert_yaxis()  # Most sensitive at the top

    ax.set_xlabel(r'Change in Longitudinal Composite Tensile Strength $\Delta \sigma_c$ (MPa) from Baseline (~1005 MPa)')
    ax.set_title(r'One-at-a-Time (OAT) Sensitivity Analysis for UD E-Glass/Epoxy ($\pm 20\%$ Variation)', pad=12)
    ax.set_xlim(-320, 320)
    ax.legend(loc='lower right', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig6_experimental_validation(output_path: str = "figures/fig6_experimental_validation.png"):
    """
    Fig 6: Model Validation Against Published Experimental Benchmarks
    Shows Classical RoM (upper bound), Modified RoM curve, and published experimental data with error bars.
    """
    apply_academic_style()
    eval_results = evaluate_models_against_benchmark()
    df_exp = eval_results["df_comparison"]
    metrics_class = eval_results["metrics_classical"]
    metrics_mod = eval_results["metrics_modified"]

    # Continuous model curves for plotting
    df_sweep = run_parametric_vf_sweep(vf_min=0.25, vf_max=0.70, num_points=100)

    fig, ax = plt.subplots(figsize=(8.8, 5.5))

    # Classical RoM (Upper bound)
    ax.plot(df_sweep["V_f"], df_sweep["sigma_c_ideal_MPa"], color=ACCENT_GRAY,
            linestyle='--', linewidth=2.2, label=r'Classical RoM (Upper Bound: 0% Voids, Perfect Alignment)')

    # Modified RoM (Nominal with envelope)
    ax.plot(df_sweep["V_f"], df_sweep["sigma_c_modified_MPa"], color=PRIMARY_BLUE,
            linewidth=2.8, label=r'Modified RoM ($\eta_\theta \cdot \eta_v \cdot \eta_w \cdot \eta_{int}$ physics model)')

    # Confidence band for Modified RoM (+- 6% to capture typical manufacturing variation)
    upper_band = df_sweep["sigma_c_modified_MPa"] * 1.06
    lower_band = df_sweep["sigma_c_modified_MPa"] * 0.94
    ax.fill_between(df_sweep["V_f"], lower_band, upper_band, color=PRIMARY_BLUE, alpha=0.15,
                    label=r'Modified RoM Expected Range ($\pm 6\%$ manufacturing variance)')

    # Plot experimental benchmark points with error bars
    ax.errorbar(
        df_exp["Fiber_Volume_Fraction"],
        df_exp["Tensile_Strength_MPa"],
        yerr=df_exp["Std_Dev_MPa"],
        fmt='s',
        markersize=7,
        color=DARK_BLUE,
        ecolor=DARK_BLUE,
        elinewidth=1.6,
        capsize=4,
        capthick=1.2,
        label=r'Published Experimental Data (ASTM D3039 / WWFE / Literature, $N=16$)'
    )

    # Inset metrics comparison box
    textbox = (
        r"$\mathbf{Model\ Validation\ Metrics:}$" + "\n"
        r"$\bullet\ \mathbf{Classical\ RoM:}$" + "\n"
        f"   MAE = {metrics_class['MAE_MPa']} MPa, MAPE = {metrics_class['MAPE_pct']}%\n"
        f"   $R^2$ = {metrics_class['R2']} (Gross overprediction)\n"
        r"$\bullet\ \mathbf{Modified\ RoM:}$" + "\n"
        f"   MAE = {metrics_mod['MAE_MPa']} MPa, MAPE = {metrics_mod['MAPE_pct']}%\n"
        f"   $R^2$ = {metrics_mod['R2']} (Excellent physical fit)"
    )
    ax.text(0.04, 0.45, textbox, transform=ax.transAxes, fontsize=9.2, verticalalignment='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8F9FA', edgecolor='#0070C0', lw=1.3))

    ax.set_title('Experimental Validation: Classical vs. Modified RoM against Published Tensile Tests', pad=12)
    ax.set_xlabel('Fiber Volume Fraction ($V_f$)')
    ax.set_ylabel('Longitudinal Tensile Strength $X_t$ (MPa)')
    ax.set_xlim(0.25, 0.70)
    ax.set_ylim(400, 2400)
    ax.legend(loc='upper left', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def generate_all_figures():
    """Generate all 6 academic figures."""
    os.makedirs("figures", exist_ok=True)
    plot_fig1_rom_strength_curve()
    plot_fig2_microstructure_schematic()
    plot_fig3_stress_strain_schematic()
    plot_fig4_knockdown_mechanisms()
    plot_fig5_sensitivity_tornado()
    plot_fig6_experimental_validation()
    print("All 6 figures successfully generated in figures/")


if __name__ == "__main__":
    generate_all_figures()
