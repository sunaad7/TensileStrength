"""
TensileCheckmate: Figure Generation Suite for 27-Slide ML + Rule of Mixtures Project
Produces all 8 academic-grade figures in Times New Roman with #0070C0 blue accents.
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

from src.ml_models import train_and_evaluate_models


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
ACCENT_RED = '#C00000'
ACCENT_GREEN = '#008040'


def plot_fig1_rom_ideal_curve(output_path: str = "figures/fig1_rom_ideal_curve.png"):
    """Slide 18: Ideal Rule of Mixtures tensile strength curve from Vf = 0.1 to 0.6."""
    apply_academic_style()
    vf = np.linspace(0.10, 0.60, 100)
    rom = 3400.0 * vf + 70.0 * (1.0 - vf)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(vf, rom, color=PRIMARY_BLUE, linewidth=2.8, label=r'Ideal RoM: $\sigma_c = \sigma_f V_f + \sigma_m (1 - V_f)$')
    ax.fill_between(vf, 0, rom, color=PRIMARY_BLUE, alpha=0.15)

    milestones = [
        (0.10, 403.0, "Vf = 0.10: 403 MPa"),
        (0.30, 1069.0, "Vf = 0.30: 1069 MPa"),
        (0.50, 1735.0, "Vf = 0.50 (Ref): 1735 MPa"),
        (0.60, 2068.0, "Vf = 0.60: 2068 MPa")
    ]
    for x_val, y_val, lbl in milestones:
        ax.plot(x_val, y_val, 'o', color=DARK_BLUE, markersize=7)
        ax.annotate(lbl, (x_val, y_val), textcoords="offset points", xytext=(-25, 12),
                    fontsize=9, weight='bold', color=DARK_BLUE,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=PRIMARY_BLUE, lw=1))

    ax.text(0.5, 0.92, '[ IDEAL ESTIMATE — NOT MEASURED EXPERIMENTAL DATA ]',
            transform=ax.transAxes, ha='center', fontsize=9.2, color='#888888',
            bbox=dict(boxstyle="square,pad=0.25", fc="#FAFAFA", ec="#CCCCCC", lw=0.8))

    ax.set_title('Ideal Rule-of-Mixtures Tensile Strength of E-Glass/Epoxy', pad=12)
    ax.set_xlabel('Fiber Volume Fraction ($V_f$)')
    ax.set_ylabel(r'Ideal Composite Tensile Strength $\sigma_c$ (MPa)')
    ax.set_xlim(0.08, 0.62)
    ax.set_ylim(0, 2400)
    ax.legend(loc='upper left')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig2_ply_structure_schematic(output_path: str = "figures/fig2_ply_structure_schematic.png"):
    """Slide 15: Schematic cross-section of a unidirectional ply at Vf ~ 0.50."""
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(7.5, 5.0))

    # Matrix block
    rect = patches.Rectangle((0, 0), 10, 7.5, linewidth=2, edgecolor='#333333', facecolor='#E9ECF2')
    ax.add_patch(rect)

    # Circular E-glass fibers (blue circles)
    r = 0.52
    dx = 1.45
    dy = 1.25

    for row, y in enumerate(np.arange(0.8, 7.0, dy)):
        offset = (dx / 2.0) if (row % 2 == 1) else 0.0
        for x in np.arange(0.8 + offset, 9.5, dx):
            c = patches.Circle((x, y), r, edgecolor=PRIMARY_BLUE, facecolor='#BDD7EE', linewidth=1.8)
            ax.add_patch(c)

    # Annotations
    ax.text(5.0, 7.0, 'Unidirectional Ply Transverse Cross-Section ($V_f \\approx 0.50$)',
            fontsize=12, weight='bold', color=DARK_BLUE, ha='center')
    ax.text(5.0, 0.4, r'$\odot$ Fiber Axis: Running into the page (tensile load acts along fiber length)',
            fontsize=9.5, color='#333333', ha='center', style='italic')

    # Legend
    legend_elements = [
        patches.Patch(facecolor='#BDD7EE', edgecolor=PRIMARY_BLUE, linewidth=1.8, label=r'E-Glass Fibers ($\sigma_f = 3400\ \mathrm{MPa},\ E_f = 72.4\ \mathrm{GPa}$)'),
        patches.Patch(facecolor='#E9ECF2', edgecolor='#333333', linewidth=1.5, label=r'Epoxy Matrix ($\sigma_m = 70\ \mathrm{MPa},\ E_m = 3.4\ \mathrm{GPa}$)')
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
    """Slide 17: Schematic stress-strain curve showing linear elastic behavior and brittle fracture."""
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.8))

    # Qualitative curves
    eps = np.linspace(0, 2.8, 100)
    stress = 380.0 * eps

    # Brittle drop
    eps_post = np.array([2.8, 2.95])
    stress_post = np.array([380.0 * 2.8, 0.0])

    eps_tot = np.concatenate([eps, eps_post])
    stress_tot = np.concatenate([stress, stress_post])

    ax.plot(eps_tot, stress_tot, color=PRIMARY_BLUE, linewidth=3.0, label='UD GFRP Tensile Response')

    # Peak stress marker
    ax.plot(2.8, 380.0 * 2.8, marker='*', markersize=14, color=ACCENT_RED)
    ax.annotate('Peak Tensile Strength\n(Brittle Fracture)',
                xy=(2.8, 380.0 * 2.8), xytext=(1.5, 950),
                arrowprops=dict(facecolor=ACCENT_RED, edgecolor=ACCENT_RED, arrowstyle='->', lw=1.6),
                fontsize=10, weight='bold', color=ACCENT_RED,
                bbox=dict(boxstyle="round,pad=0.25", fc="#FFF0F0", ec=ACCENT_RED, lw=1))

    # Linear region annotation
    ax.annotate(r'Linear Elastic Region' + '\n' + r'($\sigma = E \cdot \epsilon$)',
                xy=(1.1, 418), xytext=(0.4, 650),
                arrowprops=dict(facecolor=DARK_BLUE, edgecolor=DARK_BLUE, arrowstyle='->', lw=1.4),
                fontsize=9.5, color=DARK_BLUE, weight='bold')

    # Schematic watermark
    ax.text(0.5, 0.92, '[ SCHEMATIC REPRESENTATION — NOT MEASURED EXPERIMENTAL DATA ]',
            transform=ax.transAxes, ha='center', fontsize=9.2, color='#888888',
            bbox=dict(boxstyle="square,pad=0.25", fc="#FAFAFA", ec="#CCCCCC", lw=0.8))

    ax.set_title('Schematic Tensile Stress–Strain Curve of GFRP Composite', pad=12)
    ax.set_xlabel(r'Tensile Strain ($\epsilon$) $\longrightarrow$ [No Plastic Yielding]')
    ax.set_ylabel(r'Tensile Stress ($\sigma$) $\longrightarrow$ [Catastrophic Rupture at Peak]')

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(0, 3.5)
    ax.set_ylim(0, 1250)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig4_why_strength_falls_short(output_path: str = "figures/fig4_why_strength_falls_short.png"):
    """Slide 7: Why measured strength falls short (4 factors pointing to measured strength)."""
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(9.2, 5.2))

    # Left: Ideal RoM box
    box_ideal = patches.FancyBboxPatch((0.5, 3.8), 3.0, 1.2, boxstyle="round,pad=0.2",
                                      fc='#D9E1F2', ec=PRIMARY_BLUE, lw=2.2)
    ax.add_patch(box_ideal)
    ax.text(2.0, 4.6, r'Ideal RoM Estimate' + '\n' + r'$\sigma_c = \sigma_f V_f + \sigma_m (1 - V_f)$',
            ha='center', va='center', fontsize=10.5, weight='bold', color=DARK_BLUE)
    ax.text(2.0, 4.05, r'Baseline at $V_f=0.50$: $\mathbf{1735\ \mathrm{MPa}}$',
            ha='center', va='center', fontsize=9.5, weight='bold', color=PRIMARY_BLUE)

    # Center: 4 factors
    factors = [
        ("1. Micro-Voids & Porosity", "Reduces load-carrying area;\nacts as crack initiators", "#FCE4D6", "#C65911", 5.2, 4.0),
        ("2. Weak Fibre-Matrix Bonding", "Incomplete stress transfer\nfrom matrix to fibers", "#FFF2CC", "#BF8F00", 5.2, 2.7),
        ("3. Fibre Misalignment", "Wavy fibers carry less load;\ninduces off-axis shear", "#E2EFDA", "#375623", 5.2, 1.4),
        ("4. Manufacturing Variation", "Cure temperature and pressure\nchange final properties", "#F2DCDB", "#C00000", 5.2, 0.1)
    ]

    for title, desc, fc, ec, bx, by in factors:
        box = patches.FancyBboxPatch((bx, by), 3.5, 1.05, boxstyle="round,pad=0.15",
                                     fc=fc, ec=ec, lw=1.6)
        ax.add_patch(box)
        ax.text(bx + 0.15, by + 0.8, title, fontsize=9.2, weight='bold', color=ec)
        ax.text(bx + 0.15, by + 0.38, desc, fontsize=8.0, color='#333333', va='center')

        # Connect ideal to factors
        ax.annotate('', xy=(bx, by + 0.52), xytext=(3.65, 4.4),
                    arrowprops=dict(arrowstyle='->', color='#777777', lw=1.2, connectionstyle="angle3,angleA=0,angleB=-90"))
        # Connect factors to measured
        ax.annotate('', xy=(9.3, 2.4), xytext=(bx + 3.65, by + 0.52),
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1.3, connectionstyle="angle3,angleA=0,angleB=90"))

    # Right: Measured strength box
    box_meas = patches.FancyBboxPatch((9.3, 1.7), 2.9, 1.4, boxstyle="round,pad=0.2",
                                      fc='#E2EFDA', ec='#375623', lw=2.4)
    ax.add_patch(box_meas)
    ax.text(10.75, 2.65, 'Real Measured Strength\n(Below Ideal Estimate)',
            ha='center', va='center', fontsize=10.5, weight='bold', color='#276A3C')
    ax.text(10.75, 2.05, r'$\mathbf{1000\ \text{--}\ 1200\ \mathrm{MPa}}$',
            ha='center', va='center', fontsize=10.5, weight='bold', color='#1E4620')

    ax.text(6.3, 5.4, 'Why Measured Tensile Strength Falls Short of the Ideal Estimate',
            ha='center', fontsize=12.5, weight='bold', color=DARK_BLUE)

    ax.set_xlim(0.2, 12.5)
    ax.set_ylim(-0.2, 5.7)
    ax.axis('off')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig5_combining_physics_ml(output_path: str = "figures/fig5_combining_physics_ml.png"):
    """Slide 10: Combining physics with machine learning architecture diagram."""
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(9.2, 5.0))

    # 4 Inputs on Left
    inputs = [
        ("Fibre Volume Fraction (Vf)", "#D9E1F2", PRIMARY_BLUE, 0.8, 3.9),
        ("Cure Temperature (T)", "#D9E1F2", PRIMARY_BLUE, 0.8, 2.7),
        ("Consolidation Pressure (P)", "#D9E1F2", PRIMARY_BLUE, 0.8, 1.5),
        ("Rule-of-Mixtures Estimate\n[Physics Baseline: sigma_f*Vf + sigma_m*(1-Vf)]", "#FFF2CC", "#BF8F00", 0.8, 0.2)
    ]

    for lbl, fc, ec, bx, by in inputs:
        h = 0.95 if "\n" in lbl else 0.85
        box = patches.FancyBboxPatch((bx, by), 3.4, h, boxstyle="round,pad=0.15", fc=fc, ec=ec, lw=1.6)
        ax.add_patch(box)
        ax.text(bx + 1.7, by + h / 2.0, lbl, ha='center', va='center', fontsize=9.2, weight='bold', color='#222222')
        # Arrow to ML
        ax.annotate('', xy=(5.2, 2.5), xytext=(bx + 3.55, by + h / 2.0),
                    arrowprops=dict(arrowstyle='->', color=PRIMARY_BLUE, lw=1.6))

    # Center: ML Model Block
    box_ml = patches.FancyBboxPatch((5.2, 1.5), 3.0, 2.0, boxstyle="round,pad=0.2",
                                   fc='#BDD7EE', ec=DARK_BLUE, lw=2.2)
    ax.add_patch(box_ml)
    ax.text(6.7, 3.0, 'Machine Learning\nModel', ha='center', va='center', fontsize=12, weight='bold', color=DARK_BLUE)
    ax.text(6.7, 2.1, '• Linear Regression\n• Random Forest (300)\n• Gradient Boosting',
            ha='center', va='center', fontsize=9.2, color='#222222')

    # Arrow from ML to output
    ax.annotate('', xy=(9.1, 2.5), xytext=(8.35, 2.5),
                arrowprops=dict(arrowstyle='->', color=DARK_BLUE, lw=2.0))

    # Right: Predicted Strength Output
    box_out = patches.FancyBboxPatch((9.1, 1.8), 2.9, 1.4, boxstyle="round,pad=0.2",
                                    fc='#E2EFDA', ec='#375623', lw=2.4)
    ax.add_patch(box_out)
    ax.text(10.55, 2.7, 'Predicted Tensile\nStrength', ha='center', va='center', fontsize=11, weight='bold', color='#276A3C')
    ax.text(10.55, 2.1, 'Learns correction from data', ha='center', va='center', fontsize=8.5, color='#444444', style='italic')

    ax.text(6.3, 5.0, 'Combining Physics with Machine Learning Architecture',
            ha='center', fontsize=13, weight='bold', color=DARK_BLUE)

    ax.set_xlim(0.4, 12.4)
    ax.set_ylim(-0.1, 5.4)
    ax.axis('off')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig6_train_test_workflow(output_path: str = "figures/fig6_train_test_workflow.png"):
    """Slide 20: Train-test workflow (600 samples, 80/20 split, fitted on 480, scored on 120)."""
    apply_academic_style()
    fig, ax = plt.subplots(figsize=(9.2, 5.0))

    # Left: Total simulated dataset
    b_tot = patches.FancyBboxPatch((0.6, 1.8), 2.8, 2.0, boxstyle="round,pad=0.2", fc='#D9E1F2', ec=PRIMARY_BLUE, lw=2.0)
    ax.add_patch(b_tot)
    ax.text(2.0, 3.2, 'Synthetic Dataset', ha='center', va='center', fontsize=11, weight='bold', color=DARK_BLUE)
    ax.text(2.0, 2.5, '600 Specimens\n• Vf: 0.30 to 0.60\n• Cure Temp: 80 to 140°C\n• Pressure: 0.2 to 1.0 MPa\n• RoM estimate',
            ha='center', va='center', fontsize=8.8, color='#333333')

    # Split arrows
    ax.annotate('80% Split', xy=(4.6, 3.6), xytext=(3.55, 3.0),
                arrowprops=dict(arrowstyle='->', color='#0070C0', lw=1.8),
                fontsize=9.5, weight='bold', color='#0070C0')
    ax.annotate('20% Split', xy=(4.6, 1.8), xytext=(3.55, 2.4),
                arrowprops=dict(arrowstyle='->', color='#ED7D31', lw=1.8),
                fontsize=9.5, weight='bold', color='#ED7D31')

    # Training set block
    b_tr = patches.FancyBboxPatch((4.6, 2.9), 3.2, 1.5, boxstyle="round,pad=0.2", fc='#BDD7EE', ec=PRIMARY_BLUE, lw=1.8)
    ax.add_patch(b_tr)
    ax.text(6.2, 3.9, 'Training Set (480 Samples)', ha='center', va='center', fontsize=10.5, weight='bold', color=DARK_BLUE)
    ax.text(6.2, 3.35, 'Used to fit:\n• Linear Regression\n• Random Forest (300 trees)\n• Gradient Boosting',
            ha='center', va='center', fontsize=8.5, color='#222222')

    # Test set block
    b_te = patches.FancyBboxPatch((4.6, 0.9), 3.2, 1.5, boxstyle="round,pad=0.2", fc='#FCE4D6', ec='#C65911', lw=1.8)
    ax.add_patch(b_te)
    ax.text(6.2, 1.9, 'Test Set (120 Samples)', ha='center', va='center', fontsize=10.5, weight='bold', color='#A64000')
    ax.text(6.2, 1.35, 'Held-out unseen data\nUsed strictly for model\nevaluation and scoring',
            ha='center', va='center', fontsize=8.5, color='#222222')

    # Final scoring block on right
    b_score = patches.FancyBboxPatch((9.0, 1.7), 2.9, 2.0, boxstyle="round,pad=0.2", fc='#E2EFDA', ec='#375623', lw=2.2)
    ax.add_patch(b_score)
    ax.text(10.45, 3.1, 'Model Evaluation', ha='center', va='center', fontsize=11, weight='bold', color='#276A3C')
    ax.text(10.45, 2.3, 'Scored on Held-Out Test Set:\n• R² (Explained Variance)\n• RMSE (MPa)\n• MAE (MPa)',
            ha='center', va='center', fontsize=9.0, color='#222222')

    # Arrows to evaluation
    ax.annotate('', xy=(9.0, 2.9), xytext=(7.95, 3.5), arrowprops=dict(arrowstyle='->', color='#0070C0', lw=1.6))
    ax.annotate('', xy=(9.0, 2.2), xytext=(7.95, 1.5), arrowprops=dict(arrowstyle='->', color='#ED7D31', lw=1.6))

    ax.text(6.3, 4.8, 'Train–Test Evaluation Workflow (Synthetic Data, Random Seed = 42)',
            ha='center', fontsize=12.5, weight='bold', color=DARK_BLUE)

    ax.set_xlim(0.2, 12.3)
    ax.set_ylim(0.4, 5.2)
    ax.axis('off')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig7_model_comparison_r2(output_path: str = "figures/fig7_model_comparison_r2.png"):
    """Slide 22: Model comparison R² bar chart with negative bar range widened."""
    apply_academic_style()
    models = ['Rule of Mixtures\n(No ML Baseline)', 'Linear\nRegression', 'Random Forest\n(300 trees)', 'Gradient\nBoosting']
    # Values matching Slide 21/22
    r2_values = [-0.898, 0.879, 0.853, 0.841]
    colors = ['#888888', PRIMARY_BLUE, '#1F4E79', '#2E75B6']

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    bars = ax.bar(models, r2_values, color=colors, width=0.55, edgecolor='#333333', linewidth=1.2)

    # Widened value axis so negative bar's label sits cleanly with room
    ax.set_ylim(-1.30, 1.15)
    ax.axhline(0, color='#333333', linewidth=1.2)

    for bar, val in zip(bars, r2_values):
        if val < 0:
            ax.text(bar.get_x() + bar.get_width() / 2.0, val - 0.12, f"R² = {val:.3f}",
                    ha='center', va='top', fontsize=9.5, weight='bold', color='#C00000',
                    bbox=dict(boxstyle="round,pad=0.2", fc="#FFF0F0", ec="#C00000", lw=0.8))
        else:
            ax.text(bar.get_x() + bar.get_width() / 2.0, val + 0.05, f"R² = {val:.3f}",
                    ha='center', va='bottom', fontsize=9.5, weight='bold', color=DARK_BLUE,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=PRIMARY_BLUE, lw=0.8))

    ax.text(0.5, 0.94, '[ EVALUATED ON HELD-OUT SYNTHETIC TEST SET (N = 120) ]',
            transform=ax.transAxes, ha='center', fontsize=9.0, color='#777777',
            bbox=dict(boxstyle="square,pad=0.25", fc="#FAFAFA", ec="#DDDDDD", lw=0.8))

    ax.set_title('Model Comparison: R² on Synthetic Test Data', pad=12)
    ax.set_ylabel('Coefficient of Determination ($R^2$)')
    ax.grid(True, axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def plot_fig8_predicted_vs_actual(output_path: str = "figures/fig8_predicted_vs_actual.png"):
    """Slide 23: Predicted vs actual strength scatter plots for LR, RF, and GB."""
    apply_academic_style()
    res = train_and_evaluate_models()
    y_test = res["y_test"]
    preds = res["predictions"]

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.2), sharey=True)
    model_configs = [
        ('Linear Regression (R² = 0.88)', preds['lr'], PRIMARY_BLUE, axes[0]),
        ('Random Forest (R² = 0.85)', preds['rf'], '#1F4E79', axes[1]),
        ('Gradient Boosting (R² = 0.84)', preds['gb'], '#2E75B6', axes[2])
    ]

    min_val = min(np.min(y_test), min(np.min(p) for _, p, _, _ in model_configs)) - 50.0
    max_val = max(np.max(y_test), max(np.max(p) for _, p, _, _ in model_configs)) + 50.0

    for title, y_pred, color, ax in model_configs:
        ax.scatter(y_test, y_pred, color=color, alpha=0.75, edgecolors='white', s=55, label='Test Samples (N=120)')
        # Dashed 1:1 identity line
        ax.plot([min_val, max_val], [min_val, max_val], color='#C00000', linestyle='--', linewidth=1.8, label='Ideal 1:1 Line')
        ax.set_title(title, fontsize=11, weight='bold')
        ax.set_xlabel('Actual Tensile Strength (MPa)')
        ax.set_xlim(min_val, max_val)
        ax.set_ylim(min_val, max_val)
        ax.grid(True, linestyle='--', alpha=0.35)
        ax.legend(loc='upper left', fontsize=8.5)

    axes[0].set_ylabel('Predicted Tensile Strength (MPa)')
    fig.suptitle('Predicted vs. Actual Tensile Strength on Held-Out Synthetic Test Data', fontsize=13, weight='bold', y=1.02)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Generated {output_path}")


def generate_all_ml_figures():
    os.makedirs("figures", exist_ok=True)
    plot_fig1_rom_ideal_curve()
    plot_fig2_ply_structure_schematic()
    plot_fig3_stress_strain_schematic()
    plot_fig4_why_strength_falls_short()
    plot_fig5_combining_physics_ml()
    plot_fig6_train_test_workflow()
    plot_fig7_model_comparison_r2()
    plot_fig8_predicted_vs_actual()
    print("All 8 ML figures generated successfully in figures/")


if __name__ == "__main__":
    generate_all_ml_figures()

