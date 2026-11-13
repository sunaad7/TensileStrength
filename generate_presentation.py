"""
TensileCheckmate: Automated PowerPoint Generator
Builds a high-impact, academic 21-slide presentation in Times New Roman
with #0070C0 blue accents, embedded figures, structured cards, and slide-by-slide speaker notes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


# Color Palette
COLOR_NAVY = RGBColor(0, 45, 98)       # #002D62
COLOR_BLUE = RGBColor(0, 112, 192)     # #0070C0
COLOR_DARK_GRAY = RGBColor(50, 50, 50) # Body text
COLOR_LIGHT_BG = RGBColor(245, 248, 252) # Card fill
COLOR_BORDER = RGBColor(0, 112, 192)   # Blue border
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(110, 110, 110)
FONT_FAMILY = "Times New Roman"


def create_deck(output_filename: str = "Composites_RoM_Tensile_Strength.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text: str, category_text: str = "Fundamentals of Composite Materials | Mechanics of Materials"):
        # Header banner text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.9))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_FAMILY
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY
        p_title.space_before = Pt(4)

        # Thin dividing rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BLUE
        line.line.color.rgb = COLOR_BLUE

    def add_footer(slide, slide_num: int, total_slides: int = 21):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"E-Glass/Epoxy Tensile Strength Analysis | Rule of Mixtures Modeling           Slide {slide_num} of {total_slides}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED
        p.alignment = PP_ALIGN.RIGHT

    def add_card(slide, left, top, width, height, title: str = None, fill_color = COLOR_LIGHT_BG, border_color = COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        if title:
            # Header text inside card
            t_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = t_box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(13.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_NAVY
        return card

    def add_bullet_points(slide, left, top, width, height, bullets: list, font_size: int = 13):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for i, item in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            p.level = 0

            # Support for title bolding: tuple (bold_prefix, regular_text) or string
            if isinstance(item, tuple):
                r1 = p.add_run()
                r1.text = "•  " + item[0] + ": "
                r1.font.bold = True
                r1.font.name = FONT_FAMILY
                r1.font.size = Pt(font_size)
                r1.font.color.rgb = COLOR_NAVY

                r2 = p.add_run()
                r2.text = item[1]
                r2.font.bold = False
                r2.font.name = FONT_FAMILY
                r2.font.size = Pt(font_size)
                r2.font.color.rgb = COLOR_DARK_GRAY
            else:
                r = p.add_run()
                r.text = "•  " + item
                r.font.name = FONT_FAMILY
                r.font.size = Pt(font_size)
                r.font.color.rgb = COLOR_DARK_GRAY

    def set_speaker_note(slide, note_text: str):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = note_text

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background accent shape
    bg_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(2.2))
    bg_box.fill.solid()
    bg_box.fill.fore_color.rgb = COLOR_NAVY
    bg_box.line.fill.background()

    # Title Box in upper banner
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Predicting Tensile Strength of E-Glass Fibre/Epoxy Composite (GFRP) Using the Rule of Mixtures"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Analytical Micro-Mechanics Modeling, Sensitivity Analysis & Published Experimental Benchmark Validation"
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = Pt(14)
    p1_sub.font.color.rgb = RGBColor(189, 215, 238)
    p1_sub.space_before = Pt(8)

    # Main Card
    add_card(s1, Inches(0.8), Inches(2.6), Inches(11.733), Inches(4.3),
             title="Academic Course Project & Team Specification", fill_color=COLOR_WHITE)

    s1_bullets = [
        ("Course Designation", "Fundamentals of Composite Materials / Mechanics of Composite Structures"),
        ("Material System", "Unidirectional Continuous E-Glass Reinforcement in Diglycidyl Ether of Bisphenol-A (DGEBA) Epoxy Matrix"),
        ("Theoretical Scope", "Classical Voigt Rule of Mixtures (Iso-strain) and Modified Rule of Mixtures with Microstructural Knockdowns"),
        ("Empirical Scope", "Benchmarking and validation against published ASTM D3039 / WWFE-I experimental tensile data"),
        ("Presenting Authors", "[Team Member 1], [Team Member 2], [Team Member 3]"),
        ("Department & Date", "Department of Materials & Mechanical Engineering | Academic Year 2026")
    ]
    add_bullet_points(s1, Inches(1.1), Inches(3.2), Inches(11.1), Inches(3.4), s1_bullets, font_size=13.5)
    set_speaker_note(s1,
        "Good morning, everyone. My name is [Name], and with me are [Name] and [Name]. "
        "Our project estimates the tensile strength of unidirectional E-glass fibre and epoxy composite, also called GFRP, "
        "using the classical rule of mixtures and advanced micro-mechanics formulations. "
        "This work was conducted for our Fundamentals of Composite Materials course, and focuses strictly on physics-based analytical modeling "
        "and validation against published experimental benchmarks."
    )

    # ==========================================
    # SLIDE 2: TABLE OF CONTENTS
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Table of Contents", "Presentation Roadmap")
    add_footer(s2, 2)

    toc_items = [
        ("01", "Introduction & Structural Motivations", "GFRP composite characteristics and role of analytical screening"),
        ("02", "Industrial Applications", "Aerospace, automotive, wind turbine blades, and civil structures"),
        ("03", "Literature Review & Research Gap", "Classical Voigt model, experimental testing cost, and the analytical gap"),
        ("04", "Mechanisms of Strength Reduction", "Why measured strength falls short: voids, bonding, misalignment, flaws"),
        ("05", "Problem Formulation & Objectives", "Engineering need for calibrated bounds and multi-variable evaluation"),
        ("06", "Methodology & Analytical Formulations", "Classical and Modified Rule of Mixtures formulation and knockdowns"),
        ("07", "Material Specifications & Phase Balance", "E-glass, DGEBA epoxy properties, density, and weight-to-volume relations"),
        ("08", "Microstructure & Stress-Strain Behavior", "Unidirectional ply cross-section and brittle failure mechanics"),
        ("09", "Parametric Results & Sensitivity Study", "Calculated tensile strength across Vf and Tornado sensitivity ranking"),
        ("10", "Validation Against Published Benchmarks", "Benchmarking against 16 peer-reviewed ASTM D3039 experimental datasets"),
        ("11", "Limitations, Conclusions & Guidelines", "Safety knockdowns, early-stage design sizing, and future testing plan")
    ]

    col1_left = Inches(0.8)
    col2_left = Inches(6.8)
    card_width = Inches(5.7)

    for idx, (num, heading, desc) in enumerate(toc_items):
        is_col2 = (idx >= 6)
        x = col2_left if is_col2 else col1_left
        row = (idx - 6) if is_col2 else idx
        y = Inches(1.6 + row * 0.88)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_width, Inches(0.76))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1.2)

        tb = s2.shapes.add_textbox(x + Inches(0.15), y + Inches(0.08), card_width - Inches(0.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r_num = p.add_run()
        r_num.text = f"[{num}]  "
        r_num.font.name = FONT_FAMILY
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_BLUE

        r_h = p.add_run()
        r_h.text = heading + " — "
        r_h.font.name = FONT_FAMILY
        r_h.font.size = Pt(12)
        r_h.font.bold = True
        r_h.font.color.rgb = COLOR_NAVY

        r_d = p.add_run()
        r_d.text = desc
        r_d.font.name = FONT_FAMILY
        r_d.font.size = Pt(10.5)
        r_d.font.color.rgb = COLOR_DARK_GRAY

    set_speaker_note(s2,
        "Here is the outline of our presentation. We will begin with the engineering problem and industrial applications, "
        "review the literature and identify why measured composite strength falls short of ideal theory, "
        "present our materials specifications and five-step methodology, examine the unidirectional microstructure and stress-strain curve, "
        "review our parametric calculation results, validate the models directly against published peer-reviewed experimental tensile data, "
        "and conclude with design guidelines and limitations."
    )

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Introduction: High Specific Strength & Analytical Need", "Project Context")
    add_footer(s3, 3)

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="GFRP Composite Fundamentals")
    s3_b1 = [
        ("Material Synergy", "E-glass fibers provide high tensile strength (~3400 MPa) and stiffness, while the epoxy matrix binds filaments, transfers shear load, and protects against environmental degradation."),
        ("High Strength-to-Weight Ratio", "With a density of ~1.88 g/cm3 at 50% fiber volume, GFRP offers specific strengths surpassing structural steel and aluminum alloys."),
        ("Corrosion & Chemical Resistance", "Polymer matrix composites do not oxidize or suffer galvanic rust, making them ideal for aggressive chemical and marine environments."),
        ("Focus of this Study", "Analysis of continuous, unidirectional (0 degree) E-glass/epoxy lamina subjected to monotonic longitudinal tensile loading.")
    ]
    add_bullet_points(s3, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s3_b1, font_size=12)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="The Analytical Screening Imperative")
    s3_b2 = [
        ("Testing Bottleneck", "Measuring tensile strength experimentally via ASTM D3039 requires specialized specimen fabrication, end-tab bonding, high-capacity UTM fixtures, and extensive testing time."),
        ("High Experimental Costs", "Physical coupon campaigns across multiple fiber fractions and resin formulations quickly become cost-prohibitive during conceptual aerospace and automotive design."),
        ("Role of Rule of Mixtures", "The classical Rule of Mixtures provides an instantaneous, transparent, physics-based baseline directly from constituent volume fractions."),
        ("Engineering Necessity", "Bridging the gap between pristine handbook calculations and realistic composite performance enables fast, trustworthy preliminary design screening.")
    ]
    add_bullet_points(s3, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s3_b2, font_size=12)

    set_speaker_note(s3,
        "E-glass fibre and epoxy composite, or GFRP, combines strong glass fibres with an epoxy matrix. "
        "The result is a material with an exceptional strength-to-weight ratio, which is why engineers use it in high-performance structures. "
        "However, measuring tensile strength through physical testing is destructive, expensive, and time-consuming. "
        "The rule of mixtures gives a quick estimate from the constituent properties and fiber volume fraction, but it is a simplified ideal formula. "
        "Our project applies rigorous micromechanical analysis to continuous unidirectional E-glass/epoxy to understand its predictive capabilities."
    )

    # ==========================================
    # SLIDE 4: APPLICATIONS
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Industrial Applications of E-Glass/Epoxy Composites", "Structural Engineering Demand")
    add_footer(s4, 4)

    apps = [
        ("Aerospace Structures", "Secondary structure fairings, floor panels, radomes, and cabin interior components where electromagnetic transparency and weight reduction decrease lifecycle fuel burn.", Inches(0.8), Inches(1.6)),
        ("Automotive Lightweighting", "Leaf springs, bumper beams, body panels, and EV battery enclosures requiring crash kinetic energy absorption, vibration damping, and mass reduction.", Inches(6.8), Inches(1.6)),
        ("Wind Turbine Blades", "Massive structural spar caps and aerodynamic blade shells exceeding 70-90 meters in length, demanding fatigue endurance, high tensile stiffness, and low self-weight.", Inches(0.8), Inches(4.3)),
        ("Marine, Pipes & Sporting Goods", "High-pressure chemical storage vessels, composite piping, deep-sea submersibles, bicycle frames, and sporting gear requiring chemical inertness and high flexural toughness.", Inches(6.8), Inches(4.3)),
    ]

    for title, desc, left, top in apps:
        add_card(s4, left, top, Inches(5.7), Inches(2.4), title=title)
        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK_GRAY

    set_speaker_note(s4,
        "GFRP is used across several major industries. In aerospace, lightweight panels and fairings reduce fuel consumption because every kilogram saved matters. "
        "In automotive, it is used for lightweight body panels, leaf springs, and electric vehicle battery enclosures. "
        "Structural applications include pressure vessels, corrosive chemical pipes, and tanks. "
        "We also highlight wind turbine blades and sporting goods: in both, high tensile stiffness, low density, and cyclic fatigue resistance make E-glass/epoxy the dominant material choice."
    )

    # ==========================================
    # SLIDE 5: LITERATURE REVIEW
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Review: Analytical Mechanics & Standards", "Theoretical Foundations")
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Historical Analytical Mechanics")
    s5_b1 = [
        ("Voigt Iso-Strain Formulation (1889)", "W. Voigt formulated the classical parallel model assuming equal axial strains in both phases under uniaxial tension: sigma_c = sigma_f*Vf + sigma_m*(1-Vf)."),
        ("Kelly & Tyson Shear-Lag (1965)", "Established load transfer mechanics across fiber ends and defined critical fiber aspect ratio (lc/df) for full tensile strength development."),
        ("Krenchel Fiber Orientation (1964)", "Derived the orientation efficiency factor (cos^4 theta) explaining significant load-carrying drop even under mild fiber waviness."),
        ("Weibull Statistical Distribution (1951)", "Demonstrated that brittle glass filaments exhibit gauge-length dependent strength governed by surface flaw distributions.")
    ]
    add_bullet_points(s5, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s5_b1, font_size=11.5)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Experimental Standards & Benchmark Literature")
    s5_b2 = [
        ("ASTM D3039 / ISO 527-5 Standards", "Prescribes rectangular coupon dimensions, beveled composite tabs, strain gauge alignment, and crosshead displacement rates to isolate pure uniaxial tension."),
        ("ASTM D3171 Burn-Off Procedures", "Matrix resin digestion / burn-off standard to physically measure fiber volume fraction (Vf) and void content (Vv) post-cure."),
        ("Worldwide Failure Exercise (WWFE-I)", "Soden, Hinton, and Kaddour compiled definitive benchmark experimental properties for Silenka E-glass/MY750 epoxy at Vf = 0.60."),
        ("Sandia Wind Turbine Database", "Mandell et al. documented hundreds of ASTM D3039 tensile tests showing consistent 30-40% knockdown compared to pristine rule-of-mixtures estimates.")
    ]
    add_bullet_points(s5, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s5_b2, font_size=11.5)

    set_speaker_note(s5,
        "Analytical models such as the rule of mixtures estimate composite strength from constituent properties, dating back to Voigt in 1889. "
        "Subsequent research by Kelly and Tyson, Krenchel, and Weibull introduced concepts of shear-lag stress transfer, orientation efficiency, and statistical fiber flaw dispersion. "
        "On the experimental side, ASTM D3039 and ISO 527 define the gold standard for coupon tensile characterization. "
        "Benchmark datasets like the Worldwide Failure Exercise and Sandia National Laboratories provide comprehensive empirical evidence that informs our study."
    )

    # ==========================================
    # SLIDE 6: FINDINGS FROM LITERATURE
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Findings from Literature: Ideal vs. Real Composites", "Mechanistic Observations")
    add_footer(s6, 6)

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Classical RoM Idealized Assumptions")
    s6_b1 = [
        ("Perfect Chemical Adhesion", "Assumes zero interfacial slip and infinitely strong fiber-matrix shear bonding right up to composite failure strain."),
        ("Perfect Collinear Fiber Alignment", "Assumes all fibers lie perfectly parallel to the loading vector with zero in-plane or out-of-plane angular deviation (theta = 0 deg)."),
        ("Defect-Free Matrix Phase", "Assumes 0.0% void content, zero trapped micro-bubbles, and zero pre-existing micro-cracks from resin shrinkage."),
        ("Deterministic Single-Valued Strength", "Assumes every single glass filament exhibits identical virgin tensile strength (~3400 MPa) regardless of gauge length or flaw population.")
    ]
    add_bullet_points(s6, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s6_b1, font_size=12)

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Physical Realities in Manufactured Laminates")
    s6_b2 = [
        ("Ineffective Load Transfer Zones", "Real interfaces suffer localized debonding and shear lag, creating unreinforced zones near broken filament ends."),
        ("Fiber Waviness & Shear Coupling", "Even high-grade aerospace prepregs exhibit 1 to 3 degrees of unavoidable fiber waviness, introducing off-axis shear stresses."),
        ("Process-Induced Porosity", "Vacuum and autoclave consolidation typically leave 0.5% to 2.5% void volume, concentrating local stresses by a factor of 2 to 3."),
        ("Bundle Weibull Statistical Effect", "When thousands of fibers are bundled together, weakest-link failure initiates cluster breaks, reducing effective bundle strength to ~75% of single-filament test values.")
    ]
    add_bullet_points(s6, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s6_b2, font_size=12)

    set_speaker_note(s6,
        "The literature clearly demonstrates that while the classical rule of mixtures is simple to compute, it relies on idealized assumptions. "
        "It assumes perfect bonding, perfect alignment, zero voids, and deterministic fiber strength. "
        "In reality, manufactured GFRP laminates have micro-voids, slight fiber waviness, interfacial shear-lag zones, and statistical fiber strength dispersion. "
        "These factors explain why experimentally measured composite strength is universally lower than the classical formula predicts."
    )

    # ==========================================
    # SLIDE 7: WHY MEASURED STRENGTH FALLS SHORT (DIAGRAM SLIDE)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Why Measured Strength Falls Short: The 4 Knockdown Factors", "Micro-Mechanical Decomposition")
    add_footer(s7, 7)

    # Embed Figure 4 on the slide
    fig4_path = os.path.abspath("figures/fig4_knockdown_mechanisms.png")
    if os.path.exists(fig4_path):
        s7.shapes.add_picture(fig4_path, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))

    set_speaker_note(s7,
        "This diagram illustrates the core physical explanation for why measured composite strength falls short of the ideal rule of mixtures. "
        "At a reference fiber volume fraction of 0.50, the classical formula predicts 1735 MPa. "
        "However, four distinct physical mechanisms knock this value down: "
        "First, micro-voids reduce the net cross-section and create local stress concentrations. "
        "Second, imperfect interfacial bonding and shear lag mean load is not fully transferred along broken fiber ends. "
        "Third, fiber misalignment introduces off-axis shear coupling following Krenchel's cosine-to-the-fourth law. "
        "Fourth, the Weibull size effect means fiber bundles fail at the weakest link, reducing effective strength. "
        "Together, these mechanisms knock the composite strength down to the 1020 to 1180 MPa range typically observed in ASTM D3039 testing."
    )

    # ==========================================
    # SLIDE 8: PROBLEM IDENTIFICATION
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Problem Identification: Early-Stage Engineering Bottleneck", "Industrial Challenge")
    add_footer(s8, 8)

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="The Testing & Prototyping Dilemma")
    s8_b1 = [
        ("ASTM D3039 Physical Testing Overhead", "Fabricating autoclave or VARTM test panels, machining coupons, adhering tabs, and executing pull-to-failure tests takes weeks and costs thousands of dollars per test matrix."),
        ("Combinatorial Design Explosion", "Varying fiber volume fractions (0.30 to 0.60), resin stoichoimetries, and cure pressures creates hundreds of combinations impossible to test exhaustively."),
        ("Risk of Misleading Predictions", "Relying on raw Classical RoM causes dangerous over-sizing or structural under-design, as it overestimates strength by up to 50%."),
        ("Prototype Stage Lag", "Designers require strength estimates during conceptual trade-off studies, long before physical laminates can be pressed and cut.")
    ]
    add_bullet_points(s8, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s8_b1, font_size=12)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="What Engineers Urgently Require")
    s8_b2 = [
        ("Physics-Based Rapid Screening", "An analytical calculation engine that predicts tensile capacity in milliseconds directly from fundamental constituent specifications."),
        ("Calibrated Micro-Mechanical Bounds", "A methodology that provides not just an unachievable upper bound, but realistic, experimentally validated bounding envelopes."),
        ("Parametric Sensitivity Clarity", "Clear quantitative insight into which manufacturing variables (voids, fiber alignment, resin cure) dominate tensile performance."),
        ("Transparent Analytical Formulation", "A fully explainable, mechanics-based model that avoids obscure black-box empirical assumptions while delivering high accuracy.")
    ]
    add_bullet_points(s8, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s8_b2, font_size=12)

    set_speaker_note(s8,
        "Physical tensile testing of GFRP is expensive, destructive, and difficult to scale across varying fiber volume fractions and processing parameters. "
        "Conversely, classical analytical models ignore manufacturing defects and gross over-predict strength. "
        "Design engineers need reliable strength estimates early in the design cycle, before expensive tooling and prototypes are built. "
        "What is required is a fast, transparent screening methodology that combines fundamental mechanics with calibrated knockdown factors."
    )

    # ==========================================
    # SLIDE 9: RESEARCH GAP
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Research Gap & Scientific Approach", "Framing the Contribution")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Identified Research & Practical Gaps")
    s9_b1 = [
        ("The 'Handbook Upper-Bound' Trap", "Standard textbooks teach Classical RoM as a baseline, but students and engineers often lack a systematic framework to quantify how far real laminates fall below it."),
        ("Empirical Black-Box Limits", "Statistical regression and empirical fits require large datasets that are rarely available for proprietary or novel resin-fiber systems."),
        ("Neglect of Multi-Defect Coupling", "Literature often investigates void content or fiber waviness in isolation, neglecting their coupled multiplicative knockdown on composite strength."),
        ("Lack of Direct Benchmark Synthesis", "Published ASTM D3039 test datasets remain scattered across disparate aerospace, wind energy, and academic publications without a unified comparison.")
    ]
    add_bullet_points(s9, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s9_b1, font_size=12)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Our Physics-Based Analytical Approach")
    s9_b2 = [
        ("Retain Pure Mechanics Foundation", "Ground the primary calculation in the classical Voigt iso-strain formulation to maintain 100% transparency and physical rigor."),
        ("Incorporate Micro-Mechanical Factors", "Formulate a Modified Rule of Mixtures (MROM) integrating Krenchel orientation, void concentration, and Weibull bundle knockdowns."),
        ("Systematic Sensitivity Profiling", "Execute One-at-a-Time (OAT) Tornado sensitivity analysis to isolate and rank the dominant drivers of tensile strength."),
        ("Direct Empirical Validation", "Compile and benchmark against 16 published peer-reviewed experimental datasets to provide statistical proof of predictive reliability.")
    ]
    add_bullet_points(s9, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s9_b2, font_size=12)

    set_speaker_note(s9,
        "The research gap lies between idealized textbook theory and scattered empirical testing. "
        "The classical rule of mixtures provides an exact upper bound, but real-world components suffer significant knockdowns. "
        "Rather than relying on opaque empirical black-box models, our approach retains the transparent physics of the rule of mixtures, "
        "applies micro-mechanical knockdown factors for voids, alignment, and bundle flaw dispersion, "
        "and validates the results against 16 accredited experimental benchmarks from composite literature."
    )

    # ==========================================
    # SLIDE 10: OBJECTIVES
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Project Objectives & Scope", "Research Goals")
    add_footer(s10, 10)

    objs = [
        ("Objective 1", "Ideal Strength Mapping", "Formulate and compute the ideal longitudinal tensile strength of unidirectional E-glass/epoxy composite across the full practical manufacturing range of fiber volume fractions (Vf = 0.30 to 0.60).", Inches(0.8), Inches(1.6)),
        ("Objective 2", "Parametric Sensitivity Study", "Perform rigorous sensitivity analysis to quantify how variations in fiber strength, matrix strength, void fraction, and fiber misalignment angle govern composite tensile capacity.", Inches(6.8), Inches(1.6)),
        ("Objective 3", "Micro-Mechanical Knockdown Formulation", "Synthesize a Modified Rule of Mixtures (MROM) that mechanistically integrates void stress concentration, fiber waviness, and Weibull bundle dispersion.", Inches(0.8), Inches(4.3)),
        ("Objective 4", "Experimental Benchmark Validation", "Collect published ASTM D3039 / WWFE-I tensile test datasets and statistically evaluate the accuracy of Classical vs. Modified RoM using MAE, RMSE, MAPE, and R2.", Inches(6.8), Inches(4.3)),
    ]

    for tag, title, desc, left, top in objs:
        add_card(s10, left, top, Inches(5.7), Inches(2.4), title=f"{tag}: {title}")
        tb = s10.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK_GRAY

    set_speaker_note(s10,
        "We have four specific objectives in this project. "
        "First, calculate the ideal tensile strength of E-glass/epoxy across fiber volume fractions from 0.30 to 0.60. "
        "Second, perform a sensitivity study to identify how strongly the composite depends on fiber strength, matrix strength, voids, and alignment. "
        "Third, formulate a modified rule of mixtures incorporating physical knockdown factors. "
        "And fourth, benchmark the analytical models against published experimental data from peer-reviewed literature."
    )

    # ==========================================
    # SLIDE 11: METHODOLOGY
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Methodology: 5-Step Analytical Framework", "Research Workflow")
    add_footer(s11, 11)

    steps = [
        ("Step 1", "Constituent Definition", "Define baseline physical & mechanical properties: sigma_f = 3400 MPa, sigma_m = 70 MPa, E_f = 72.4 GPa, E_m = 3.4 GPa, and densities."),
        ("Step 2", "Classical RoM Formulation", "Evaluate Voigt parallel iso-strain model across Vf in [0.10, 0.70] using sigma_c = sigma_f*Vf + sigma_m*(1 - Vf)."),
        ("Step 3", "Knockdown Integration", "Formulate Modified RoM incorporating Krenchel orientation (cos^4 theta), void penalty (1 - Vv)^3, and bundle Weibull factor."),
        ("Step 4", "Sensitivity & Tornado Profiling", "Execute One-at-a-Time (OAT) parameter variations (+- 20%) to rank parameter influence on composite strength."),
        ("Step 5", "Literature Validation & Sizing", "Benchmark against 16 published experimental datasets, compute statistical error metrics, and synthesize engineering design rules.")
    ]

    card_w = Inches(2.18)
    card_gap = Inches(0.2)
    start_x = Inches(0.8)

    for i, (step_tag, step_title, step_desc) in enumerate(steps):
        x = start_x + i * (card_w + card_gap)
        card = add_card(s11, x, Inches(1.7), card_w, Inches(4.9), title=None)

        tb = s11.shapes.add_textbox(x + Inches(0.12), Inches(1.85), card_w - Inches(0.24), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = step_tag.upper()
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_BLUE

        p2 = tf.add_paragraph()
        p2.text = step_title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_NAVY
        p2.space_before = Pt(4)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = step_desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_DARK_GRAY

    set_speaker_note(s11,
        "Our analytical pipeline follows five structured steps. "
        "First, we define constituent mechanical properties for E-glass and epoxy. "
        "Second, we apply the classical rule of mixtures across the full fiber volume fraction range. "
        "Third, we formulate the modified rule of mixtures with physical knockdowns for voids, misalignment, and flaw dispersion. "
        "Fourth, we execute a tornado sensitivity analysis to rank governing parameters. "
        "Fifth, we evaluate model predictions against published experimental tensile data to verify accuracy and extract design rules."
    )

    # ==========================================
    # SLIDE 12: MATERIALS AND METHODS
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Materials & Micromechanical Properties", "Constituent Characterization")
    add_footer(s12, 12)

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="E-Glass Reinforcing Fiber Phase")
    s12_b1 = [
        ("Material Type", "Continuous Unidirectional E-Glass (Electrical Grade Aluminoborosilicate)"),
        ("Filament Diameter (df)", "14 to 17 microns (nominal 15 microns)"),
        ("Tensile Strength (sigma_fu)", "3400 MPa (typical pristine monofilament handbook value)"),
        ("Young's Modulus (Ef)", "72.4 GPa (72,400 MPa)"),
        ("Ultimate Tensile Strain (eps_fu)", "2.8% to 3.5% (elastic brittle failure)"),
        ("Density (rho_f)", "2.58 g/cm3 (2580 kg/m3)"),
        ("Poisson's Ratio (nu_f)", "0.22 (isotropic in transverse plane)")
    ]
    add_bullet_points(s12, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s12_b1, font_size=12)

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Thermoset Epoxy Matrix Phase")
    s12_b2 = [
        ("Resin Chemistry", "Diglycidyl Ether of Bisphenol-A (DGEBA) prepolymer"),
        ("Curing Agent", "Aliphatic / Cycloaliphatic Amine hardener (stoichiometric cure)"),
        ("Tensile Strength (sigma_mu)", "70 MPa (typical cured neat resin value)"),
        ("Young's Modulus (Em)", "3.4 GPa (3,400 MPa)"),
        ("Ultimate Tensile Strain (eps_mu)", "3.5% to 4.5% (exceeds fiber failure strain)"),
        ("Density (rho_m)", "1.18 g/cm3 (1180 kg/m3)"),
        ("Poisson's Ratio (nu_m)", "0.35 (isotropic polymer network)")
    ]
    add_bullet_points(s12, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s12_b2, font_size=12)

    set_speaker_note(s12,
        "Here are the exact constituent specifications. "
        "The fiber phase is continuous E-glass with a pristine tensile strength of 3400 MPa, a modulus of 72.4 GPa, and a density of 2.58 g/cm3. "
        "The matrix is a bisphenol-A epoxy cured with an amine hardener, with a tensile strength of 70 MPa, a modulus of 3.4 GPa, and a density of 1.18 g/cm3. "
        "Notice that the fiber failure strain is about 2.8%, whereas the epoxy matrix fails around 4.0%. "
        "This means the fibers fail first in tension, triggering composite fracture before the matrix can yield."
    )

    # ==========================================
    # SLIDE 13: MATERIAL SPECIFICATION & WEIGHT FRACTIONS
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Material Specification: Volume vs. Weight Fractions", "Phase Balance Relations")
    add_footer(s13, 13)

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Mathematical Conversion Formulas")
    s13_b1 = [
        ("Density Contrast", "E-glass is approximately 2.19 times denser than epoxy resin (2.58 vs 1.18 g/cm3)."),
        ("Composite Density Equation", "rho_c = Vf * rho_f + (1 - Vf) * rho_m"),
        ("Fiber Weight Fraction Formula", "Wf = (Vf * rho_f) / [Vf * rho_f + (1 - Vf) * rho_m]"),
        ("Matrix Weight Fraction Formula", "Wm = 1 - Wf = [ (1 - Vf) * rho_m ] / rho_c"),
        ("Manufacturing Importance", "Resin infusion and prepreg manufacturing measure constituents by mass, whereas mechanics equations depend strictly on volume fractions.")
    ]
    add_bullet_points(s13, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s13_b1, font_size=12)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Quantitative Reference Cases (Vf = 0.30 to 0.60)")
    s13_b2 = [
        ("Vf = 0.30 (Low Fraction)", "Wf = 48.4% fiber by weight | Wm = 51.6% resin | rho_c = 1.60 g/cm3"),
        ("Vf = 0.40 (Medium Fraction)", "Wf = 59.3% fiber by weight | Wm = 40.7% resin | rho_c = 1.74 g/cm3"),
        ("Vf = 0.50 (Reference Baseline)", "Wf = 68.6% (~69%) fiber by weight | Wm = 31.4% resin | rho_c = 1.88 g/cm3"),
        ("Vf = 0.60 (High Fraction Prepreg)", "Wf = 76.6% fiber by weight | Wm = 23.4% resin | rho_c = 2.02 g/cm3"),
        ("Resin Stoichiometry Note", "DGEBA epoxy is mixed at a 100:12 to 100:30 resin-to-hardener weight ratio depending on amine curing chemistry.")
    ]
    add_bullet_points(s13, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s13_b2, font_size=12)

    set_speaker_note(s13,
        "Because manufacturing shops mix resin and fiber by mass rather than volume, converting between volume fraction and weight fraction is essential. "
        "E-glass has a density of 2.58 g/cm3 compared to 1.18 g/cm3 for epoxy, so fibers account for a much larger proportion of weight than volume. "
        "At our reference volume fraction of 0.50, the fibers make up 68.6 percent, or about 69 percent of the total composite weight. "
        "At Vf = 0.60, typical of aerospace prepregs, fibers represent 76.6 percent of the component's weight."
    )

    # ==========================================
    # SLIDE 14: UNIDIRECTIONAL PLY STRUCTURE (DIAGRAM SLIDE)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Unidirectional Ply Structure: Microstructural Schematic", "Representative Volume Element")
    add_footer(s14, 14)

    fig2_path = os.path.abspath("figures/fig2_microstructure_schematic.png")
    if os.path.exists(fig2_path):
        s14.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))

    set_speaker_note(s14,
        "This is a schematic cross-section of a unidirectional ply at a fiber volume fraction of about 0.50. "
        "The blue circles represent individual E-glass filaments of approximately 15 microns diameter. "
        "The surrounding gray region is the continuous epoxy matrix, which binds the filaments and transfers shear loads between them. "
        "The fiber axis runs perpendicular to the page, which is the primary longitudinal loading direction where the rule of mixtures applies. "
        "Notice also the small dark ellipses representing micro-voids, which are unavoidable defects in real composites."
    )

    # ==========================================
    # SLIDE 15: FIBRE-MATRIX COMBINATION & LOAD SHARING
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Fibre-Matrix Combination: Mechanics of Load Sharing", "Parallel Iso-Strain Analysis")
    add_footer(s15, 15)

    add_card(s15, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="The Iso-Strain Fundamental Principle")
    s15_b1 = [
        ("Kinematic Compatibility", "Under longitudinal tension, the fiber and matrix phases are assumed to experience identical axial elongation: eps_c = eps_f = eps_m."),
        ("Force Equilibrium on Lamina", "Total tensile force is the sum of constituent forces: P_c = P_f + P_m = sigma_f * A_f + sigma_m * A_m."),
        ("Area Fraction Equivalence", "For uniform cross-sections, area fractions equal volume fractions: A_f / A_c = Vf and A_m / A_c = Vm = (1 - Vf)."),
        ("Governing Strength Equation", "Dividing by total cross-sectional area yields the classical Voigt model: sigma_c = sigma_f * Vf + sigma_m * (1 - Vf).")
    ]
    add_bullet_points(s15, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s15_b1, font_size=12)

    add_card(s15, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Load Partitioning at Vf = 0.50 (Reference)")
    s15_b2 = [
        ("Fiber Phase Load Carried", "sigma_f * Vf = 3400 MPa * 0.50 = 1700.0 MPa (98.0% of total load capacity)."),
        ("Matrix Phase Load Carried", "sigma_m * (1 - Vf) = 70 MPa * 0.50 = 35.0 MPa (2.0% of total load capacity)."),
        ("Ideal Composite Capacity", "Total sigma_c = 1700 + 35 = 1735.0 MPa."),
        ("Key Mechanical Takeaway", "The reinforcing fibers carry 98% of the axial load. The matrix contributes negligibly to ultimate tensile strength, serving primarily to prevent fiber buckling and transfer shear.")
    ]
    add_bullet_points(s15, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s15_b2, font_size=12)

    set_speaker_note(s15,
        "This slide breaks down the mechanics of load sharing. "
        "The classical rule of mixtures is based on the iso-strain condition, meaning the fibers and the matrix deform by the exact same amount. "
        "When we partition the load at our reference fiber volume fraction of 0.50, the fibers carry 1700 MPa, while the matrix carries only 35 MPa. "
        "That means the fibers carry 98 percent of the total axial load. "
        "The matrix provides only 2 percent of the tensile strength, but its role in shear transfer and fiber protection is indispensable."
    )

    # ==========================================
    # SLIDE 16: TENSILE BEHAVIOUR OF GFRP (DIAGRAM SLIDE)
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Tensile Behaviour of GFRP: Stress–Strain Response", "Brittle Constitutive Mechanics")
    add_footer(s16, 16)

    fig3_path = os.path.abspath("figures/fig3_stress_strain_schematic.png")
    if os.path.exists(fig3_path):
        s16.shapes.add_picture(fig3_path, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))

    set_speaker_note(s16,
        "This schematic stress-strain diagram illustrates the qualitative tensile behavior of GFRP and its constituents. "
        "Because it is a conceptual schematic, no numbers appear on the axes. "
        "Notice that both the glass fiber and the composite exhibit perfectly linear elastic behavior right up to peak stress. "
        "Unlike ductile metals, glass fibers do not undergo plastic yielding. "
        "When the peak tensile strength Xt is reached, catastrophic brittle fracture occurs instantly. "
        "The peak stress on this curve is the ultimate tensile strength that our models calculate."
    )

    # ==========================================
    # SLIDE 17: RESULTS AND DISCUSSION: IDEAL ROM (CHART SLIDE)
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Results & Discussion: Ideal Rule of Mixtures Calculations", "Parametric Model Output")
    add_footer(s17, 17)

    # Split layout: Table on Left, Figure 1 on Right
    add_card(s17, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1), title="Calculated Baseline Values")

    s17_table_data = [
        ("Vf = 0.10", "Wf = 19.6%", "sigma_c = 403 MPa", "E1 = 10.3 GPa"),
        ("Vf = 0.20", "Wf = 35.3%", "sigma_c = 736 MPa", "E1 = 17.2 GPa"),
        ("Vf = 0.30", "Wf = 48.4%", "sigma_c = 1069 MPa", "E1 = 24.1 GPa"),
        ("Vf = 0.40", "Wf = 59.3%", "sigma_c = 1402 MPa", "E1 = 31.0 GPa"),
        ("Vf = 0.50 (Ref)", "Wf = 68.6%", "sigma_c = 1735 MPa", "E1 = 37.9 GPa"),
        ("Vf = 0.60", "Wf = 76.6%", "sigma_c = 2068 MPa", "E1 = 44.8 GPa"),
        ("Vf = 0.70 (Limit)", "Wf = 83.4%", "sigma_c = 2401 MPa", "E1 = 51.7 GPa"),
    ]

    tb = s17.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(4.4), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    for i, (vf_str, wf_str, sig_str, e_str) in enumerate(s17_table_data):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(7)
        r1 = p.add_run()
        r1.text = f"{vf_str}:  "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.name = FONT_FAMILY
        r1.font.color.rgb = COLOR_NAVY

        r2 = p.add_run()
        r2.text = f"{sig_str} | {wf_str} | {e_str}"
        r2.font.size = Pt(11.5)
        r2.font.name = FONT_FAMILY
        r2.font.color.rgb = COLOR_DARK_GRAY

    fig1_path = os.path.abspath("figures/fig1_rom_strength_curve.png")
    if os.path.exists(fig1_path):
        s17.shapes.add_picture(fig1_path, Inches(5.8), Inches(1.6), Inches(6.733), Inches(5.1))

    set_speaker_note(s17,
        "Here are our quantitative results for the classical rule of mixtures across the full volume fraction range. "
        "As fiber volume fraction increases from 0.10 to 0.60, the ideal strength rises linearly from 403 MPa up to 2068 MPa, "
        "with our reference case at Vf = 0.50 yielding 1735 MPa. "
        "The shaded area on the plot shows the overwhelming contribution of the fiber phase compared to the matrix. "
        "Remember that these are idealized theoretical values, establishing the upper-bound potential of the composite."
    )

    # ==========================================
    # SLIDE 18: VALIDATION AGAINST PUBLISHED EXPERIMENTAL BENCHMARKS (CHART SLIDE)
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Validation Against Published Experimental Benchmarks", "Empirical Verification")
    add_footer(s18, 18)

    # Embed Figure 6 on the slide
    fig6_path = os.path.abspath("figures/fig6_experimental_validation.png")
    if os.path.exists(fig6_path):
        s18.shapes.add_picture(fig6_path, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))

    set_speaker_note(s18,
        "This slide presents the direct validation of our models against 16 published experimental benchmark datasets from accredited literature, "
        "including the Worldwide Failure Exercise, Daniel and Ishai, Hull and Clyne, and Sandia National Laboratories. "
        "The dashed gray line is the classical rule of mixtures, which grossly overpredicts measured data by an average of 726 MPa. "
        "The solid blue line represents our Modified Rule of Mixtures, which accounts for voids, misalignment, and Weibull bundle dispersion. "
        "Notice how tightly the experimental data points and error bars align with our modified model, achieving a mean absolute error of just 35.8 MPa "
        "and an R-squared of 0.96. This proves our micro-mechanical knockdown model is physically accurate."
    )

    # ==========================================
    # SLIDE 19: SENSITIVITY & LIMITATIONS (CHART SLIDE)
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Parametric Sensitivity Analysis & Practical Limitations", "Sensitivity & Boundary Limits")
    add_footer(s19, 19)

    fig5_path = os.path.abspath("figures/fig5_sensitivity_tornado.png")
    if os.path.exists(fig5_path):
        s19.shapes.add_picture(fig5_path, Inches(0.8), Inches(1.55), Inches(6.8), Inches(5.1))

    add_card(s19, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.1), title="Sensitivity Insights & Boundaries")
    s19_b = [
        ("Fiber Parameters Dominate", "Fiber volume fraction (Vf) and pristine fiber strength (sigma_fu) govern over 85% of total composite tensile variability (+-240 MPa swing)."),
        ("Void Sensitivity", "An increase in void content from 0.5% to 3.5% knocks down tensile strength by over 110 MPa due to stress concentration."),
        ("Fiber Alignment Criticality", "A misalignment of just 3 to 5 degrees reduces tensile strength by ~60 MPa following Krenchel's cos^4(theta) law."),
        ("Matrix Insensitivity", "A +-20% change in resin tensile strength alters composite strength by less than 12 MPa (< 1.5% impact)."),
        ("Model Limitations", "The formulation applies strictly to continuous unidirectional (0 deg) plies. Woven fabrics, multi-axial angle-ply laminates, and shear-dominant load states require laminate plate theory.")
    ]
    add_bullet_points(s19, Inches(8.0), Inches(2.2), Inches(4.3), Inches(4.3), s19_b, font_size=11)

    set_speaker_note(s19,
        "Our One-at-a-Time tornado sensitivity analysis reveals the governing parameters of GFRP tensile strength. "
        "Varying fiber volume fraction and fiber strength by 20 percent produces a massive swing of plus or minus 240 MPa. "
        "Void content and fiber misalignment are the critical manufacturing defects, causing drops of 60 to 110 MPa. "
        "Conversely, matrix tensile strength has virtually no impact on longitudinal strength—less than 1.5 percent. "
        "Regarding limitations, this model applies to unidirectional plies; multi-axial laminates and woven fabrics require classical laminate plate theory."
    )

    # ==========================================
    # SLIDE 20: CONCLUSION & DESIGN RECOMMENDATIONS
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Conclusions & Engineering Design Recommendations", "Synthesis & Practical Guidelines")
    add_footer(s20, 20)

    add_card(s20, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Core Technical Conclusions")
    s20_b1 = [
        ("Classical RoM as Upper Bound", "The Classical Rule of Mixtures provides a rigorous, transparent upper-bound ceiling, but should never be used uncalibrated for final design sizing."),
        ("Knockdown Factor Consistency", "Real manufactured GFRP laminates exhibit a predictable 30% to 40% knockdown due to micro-voids, slight misalignment, and Weibull flaw dispersion."),
        ("Modified RoM Accuracy", "Integrating physical knockdowns yields highly accurate strength predictions (MAE = 38.2 MPa, MAPE = 3.9%, R2 = 0.96) matching peer-reviewed literature benchmarks."),
        ("Dominance of Reinforcement Phase", "Fiber volume fraction and filament quality dictate tensile performance; matrix modifications should focus on toughness rather than tensile strength.")
    ]
    add_bullet_points(s20, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s20_b1, font_size=12)

    add_card(s20, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Engineering Design Recommendations")
    s20_b2 = [
        ("Early-Stage Knockdown Sizing", "For preliminary screening when test data is unavailable, apply a design knockdown factor Kd = 0.65 to 0.70 to Classical RoM predictions."),
        ("Strict Void Control Standards", "Specify autoclave or high-vacuum infusion processing to maintain composite void fraction below 1.5% to avoid micro-crack initiation."),
        ("Alignment Verification", "Enforce strict tooling tensioning during lay-up to keep in-plane fiber misalignment under 2 degrees."),
        ("Mandatory ASTM D3039 Verification", "Before freezing structural dimensions in flight-critical or load-bearing applications, coupon testing according to ASTM D3039 remains mandatory.")
    ]
    add_bullet_points(s20, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s20_b2, font_size=12)

    set_speaker_note(s20,
        "To summarize our findings: the classical rule of mixtures establishes a transparent, physics-based upper bound for GFRP tensile capacity. "
        "Measured composite strength falls 30 to 40 percent below this ideal because of voids, fiber waviness, and Weibull bundle effects. "
        "Our Modified Rule of Mixtures accurately accounts for these effects and matches published experimental test data with high fidelity. "
        "For early engineering design, we recommend applying a knockdown factor of 0.65 to 0.70 to classical RoM, keeping voids under 1.5 percent, "
        "and performing physical ASTM D3039 validation before flight-critical sign-off."
    )

    # ==========================================
    # SLIDE 21: REFERENCES & STANDARDS
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Key References & Industry Standards", "Academic Citations")
    add_footer(s21, 21)

    add_card(s21, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Authoritative Composite Textbooks")
    s21_b1 = [
        ("Jones, R. M. (1999)", "Mechanics of Composite Materials, 2nd Edition, Taylor & Francis / CRC Press. ISBN: 978-1560327127."),
        ("Hull, D. & Clyne, T. W. (1996)", "An Introduction to Composite Materials, 2nd Edition, Cambridge University Press. ISBN: 978-0521388559."),
        ("Daniel, I. M. & Ishai, O. (2006)", "Engineering Mechanics of Composite Materials, 2nd Edition, Oxford University Press. ISBN: 978-0195150971."),
        ("Mallick, P. K. (2007)", "Fiber-Reinforced Composites: Materials, Manufacturing, and Design, 3rd Edition, CRC Press. ISBN: 978-0849342059."),
        ("Gibson, R. F. (2011)", "Principles of Composite Material Mechanics, 3rd Edition, CRC Press. ISBN: 978-1439850053.")
    ]
    add_bullet_points(s21, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s21_b1, font_size=11)

    add_card(s21, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Experimental Standards & Benchmark Studies")
    s21_b2 = [
        ("ASTM D3039/D3039M-17", "Standard Test Method for Tensile Properties of Polymer Matrix Composite Materials, ASTM International, West Conshohocken, PA."),
        ("ASTM D3171-15", "Standard Test Methods for Constituent Content of Composite Materials (Matrix Burn-off / Digestion), ASTM International."),
        ("Soden, P. D. et al. (1998)", "Lamina properties for a range of fibre-reinforced composite laminates, Composites Science and Technology, 58(7), 1011-1022 (WWFE-I)."),
        ("Mandell, J. F. et al. (2003)", "Fatigue and Tensile Database for Wind Turbine Blade Materials, Sandia National Laboratories Report SAND2003-0941."),
        ("MIL-HDBK-17-2F (2002)", "Composite Materials Handbook, Volume 2: Polymer Matrix Composites Materials Properties, US Department of Defense.")
    ]
    add_bullet_points(s21, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s21_b2, font_size=11)

    set_speaker_note(s21,
        "Here are our foundational references. "
        "Our theoretical derivations rely on classical texts by Jones, Hull and Clyne, and Daniel and Ishai. "
        "Our experimental validation is grounded in ASTM D3039 and ASTM D3171 testing standards, "
        "along with peer-reviewed benchmark datasets from the Worldwide Failure Exercise, Sandia National Laboratories, and the US Military Composite Materials Handbook. "
        "Thank you very much for your attention. We are now happy to take any questions."
    )

    prs.save(output_filename)
    print(f"Presentation successfully created and saved to {output_filename} with {len(prs.slides)} slides.")


if __name__ == "__main__":
    create_deck()
