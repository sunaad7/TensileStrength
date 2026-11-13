"""
TensileCheckmate: 27-Slide PowerPoint Presentation Generator
Builds Composites_ML_Tensile_Strength_expanded.pptx in Times New Roman
with #0070C0 blue outline diagram boxes, embedded figures, and word-for-word speaker notes on all 27 slides.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


# Professional Academic Palette
COLOR_NAVY = RGBColor(0, 45, 98)          # #002D62
COLOR_BLUE = RGBColor(0, 112, 192)        # #0070C0
COLOR_DARK_GRAY = RGBColor(40, 40, 40)    # Primary text
COLOR_LIGHT_BG = RGBColor(245, 248, 252)  # Card fill
COLOR_BORDER = RGBColor(0, 112, 192)      # Blue border outline
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(110, 110, 110)
FONT_FAMILY = "Times New Roman"


def build_expanded_deck(output_filename: str = "Composites_ML_Tensile_Strength_expanded.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text: str, category_text: str = "Fundamentals of Composite Materials | Machine Learning Project"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
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
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY
        p_title.space_before = Pt(3)

        # Thin dividing rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BLUE
        line.line.color.rgb = COLOR_BLUE

    def add_footer(slide, slide_num: int, total_slides: int = 27):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.35))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"GFRP Tensile Strength: Machine Learning & Rule of Mixtures           Slide {slide_num} of {total_slides}"
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
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(13.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_NAVY
        return card

    def add_bullets(slide, left, top, width, height, bullets: list, font_size: int = 12.5):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for i, item in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(7)

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

    def set_note(slide, note: str):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = note

    # ==========================================
    # SLIDE 1: Title
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(2.2))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_NAVY
    bg.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Predicting Tensile Strength of E-glass Fibre/Epoxy Composite (GFRP) Using Machine Learning and the Rule of Mixtures"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Physics-Informed Machine Learning for Composite Mechanical Property Estimation"
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = Pt(14)
    p1_sub.font.color.rgb = RGBColor(189, 215, 238)
    p1_sub.space_before = Pt(8)

    add_card(s1, Inches(0.8), Inches(2.55), Inches(11.733), Inches(4.35),
             title="Academic Presentation & Project Metadata", fill_color=COLOR_WHITE)

    s1_bullets = [
        ("Course Designation", "Fundamentals of Composite Materials"),
        ("Material System", "Unidirectional Continuous E-Glass Reinforcement in Epoxy Matrix"),
        ("Methodology", "Hybrid Modeling combining Analytical Rule of Mixtures with Machine Learning"),
        ("Machine Learning Models", "Linear Regression, Random Forest (300 trees), Gradient Boosting"),
        ("Presenting Authors", "[Name], [Name], and [Name]"),
        ("Simulation Dataset", "600 Simulated Specimens (80/20 Train/Test Split) with Process Variation")
    ]
    add_bullets(s1, Inches(1.1), Inches(3.2), Inches(11.1), Inches(3.4), s1_bullets, font_size=13)
    set_note(s1, "Good morning, everyone. My name is [Name], and with me are [Name] and [Name]. Our project is about predicting the tensile strength of E-glass fibre and epoxy composites, also called GFRP, using machine learning and the rule of mixtures. This work was done for our Fundamentals of Composite Materials course.")

    # ==========================================
    # SLIDE 2: Table of Contents
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Table of Contents", "Presentation Outline")
    add_footer(s2, 2)

    toc_items = [
        ("1. Introduction & Applications", "Overview of GFRP, aerospace, automotive, wind turbine, and sports uses"),
        ("2. Literature Review & Findings", "Classical analytical models, assumptions, and why measured strength falls short"),
        ("3. Problem Identification & Gap", "The cost of testing and combining physics models with machine learning"),
        ("4. Objectives & Methodology", "Project goals, feature engineering, and the 5-step analysis pipeline"),
        ("5. Materials & Microstructure", "Constituent properties, weight fractions, ply cross-section, and stress-strain curve"),
        ("6. Dataset & Simulation Setup", "600 simulated specimens, cure parameters, pressure, and train-test workflow"),
        ("7. Simulation Results & Comparison", "Test scores (R², RMSE, MAE), model comparison chart, and predicted vs actual plots"),
        ("8. Limitations & Conclusions", "Synthetic data caveats, design screening use, future physical validation, references")
    ]
    for idx, (h, desc) in enumerate(toc_items):
        y = Inches(1.6 + idx * 0.65)
        card = add_card(s2, Inches(0.8), y, Inches(11.733), Inches(0.55), title=None)
        tb = s2.shapes.add_textbox(Inches(1.0), y + Inches(0.08), Inches(11.3), Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = h + ": "
        r1.font.bold = True
        r1.font.name = FONT_FAMILY
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_GRAY

    set_note(s2, "Here is the outline. I will start with the problem and the literature, then explain our method and materials. After that, we will look at the results, which are based on simulated data, and finish with the limitations, the conclusion, and our references.")

    # ==========================================
    # SLIDE 3: Introduction
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Introduction: High Specific Strength & Analytical Challenges", "Background")
    add_footer(s3, 3)

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="GFRP Composite System")
    s3_b1 = [
        ("Material Combination", "E-glass fibre and epoxy composite (GFRP) combines strong glass fibres with a protective epoxy matrix."),
        ("High Strength-to-Weight Ratio", "The result is a lightweight structural material with a high strength-to-weight ratio, which is why engineers use it."),
        ("Physical Testing Bottleneck", "Measuring tensile strength through physical testing is expensive, destructive, and time-consuming."),
        ("Rule of Mixtures Role", "The rule of mixtures gives a quick estimate from fibre volume fraction and constituent properties, but it is a simplified formula.")
    ]
    add_bullets(s3, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s3_b1)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Project Scope & Hybrid Approach")
    s3_b2 = [
        ("Unidirectional Focus", "Our project specifically studies continuous unidirectional E-glass and epoxy composites under axial tension."),
        ("Three Processing Inputs", "Predicts tensile strength from three primary inputs: fibre volume fraction, cure temperature, and pressure."),
        ("Physics + ML Integration", "Uses machine learning to capture the manufacturing corrections that simple analytical formulas miss."),
        ("Early Screening Capability", "Provides rapid strength estimation before committing to physical prototyping.")
    ]
    add_bullets(s3, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s3_b2)
    set_note(s3, "E-glass fibre and epoxy composite, or GFRP, combines strong glass fibres with an epoxy matrix. The result is a material with a high strength-to-weight ratio, which is why engineers use it. The problem is that measuring its tensile strength through physical testing is expensive and time-consuming. The rule of mixtures gives a quick estimate from the fibre volume fraction and the properties of each constituent, but it is a simple formula. Our project studies unidirectional E-glass and epoxy, and uses machine learning to predict tensile strength from three inputs: fibre volume fraction, cure temperature, and pressure.")

    # ==========================================
    # SLIDE 4: Application
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Industrial Applications of E-Glass/Epoxy GFRP", "Engineering Demand")
    add_footer(s4, 4)

    apps = [
        ("Aerospace Structures", "Lightweight panels, fairings, and radomes help reduce fuel use because every gram saved matters in flight operations.", Inches(0.8), Inches(1.6)),
        ("Automotive Components", "Used for lightweight body panels, leaf springs, and bumper parts to reduce vehicle curb weight and improve efficiency.", Inches(6.8), Inches(1.6)),
        ("Structural & Piping", "Load-bearing parts with low self-weight, such as chemical pipes, storage tanks, and corrosion-resistant infrastructure.", Inches(0.8), Inches(4.3)),
        ("Sporting Goods & Wind Blades", "Added sporting goods (bicycles, racquets) and wind turbine blades, where high tensile stiffness, low weight, and fatigue durability are critical.", Inches(6.8), Inches(4.3))
    ]
    for title, desc, l, t in apps:
        add_card(s4, l, t, Inches(5.7), Inches(2.4), title=title)
        tb = s4.shapes.add_textbox(l + Inches(0.2), t + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK_GRAY

    set_note(s4, "GFRP is used in several areas. In aerospace, lightweight panels and fairings help reduce fuel use, because every gram saved matters. In automotive, it is used for lightweight body panels and parts. Structural uses include load-bearing parts with low self-weight, such as pipes and tanks. We have also added sporting goods and wind turbine blades. In both, stiffness and low weight are important, so the same material choice applies.")

    # ==========================================
    # SLIDE 5: Literature review
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Review: Analytical Models vs. Testing", "State of the Art")
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Analytical Composite Formulations")
    s5_b1 = [
        ("Constituent Modeling", "Analytical models such as the rule of mixtures estimate composite strength directly from constituent properties."),
        ("Theoretical Foundation", "References cover classical mechanics (Voigt, Jones, Hull & Clyne) describing parallel load sharing."),
        ("Instantaneous Calculation", "Formulas provide immediate upper-bound estimates without requiring experimental specimens."),
        ("Limitation of Simplicity", "Simple formulas cannot account for fabrication nuances or environmental processing shifts.")
    ]
    add_bullets(s5, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s5_b1)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Experimental Testing Trade-offs")
    s5_b2 = [
        ("High Testing Precision", "Experimental tensile testing gives accurate values for specific coupon batches under controlled conditions."),
        ("Combinatorial Bottleneck", "Every new combination of materials, cure cycles, and pressures has to be tested separately."),
        ("Driver for Rapid Methods", "High testing cost and turnaround time is the main reason we want a faster computational prediction method."),
        ("Ongoing Review", "The full literature table, with at least thirty research articles, is being compiled by the team.")
    ]
    add_bullets(s5, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s5_b2)
    set_note(s5, "Analytical models such as the rule of mixtures estimate composite strength from the properties of the constituents, and our references cover them. Experimental tensile testing gives accurate values, but every new combination of materials and conditions has to be tested separately. That is the main reason we want a faster method. The full literature table, with at least thirty research articles, is still being completed by the team.")

    # ==========================================
    # SLIDE 6: Findings from literature
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Findings from Literature: Ideal Assumptions vs. Real Effects", "Mechanistic Insights")
    add_footer(s6, 6)

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Classical Rule-of-Mixtures Assumptions")
    s6_b1 = [
        ("Simple Computation", "The rule of mixtures is simple to compute and physically intuitive."),
        ("Ideal Interfacial Bonding", "Assumes complete, perfect bonding between fibre and matrix without shear slip."),
        ("Perfect Collinear Alignment", "Assumes perfectly parallel fibres oriented along the loading direction."),
        ("Zero Defects Assumed", "Assumes completely void-free resin and uniform flaw-free constituent properties.")
    ]
    add_bullets(s6, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s6_b1)

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Real Composite Phenomena & ML Role")
    s6_b2 = [
        ("Manufacturing Nuances", "Real composites show effects such as voids, resin pockets, and processing variation."),
        ("Formula Shortcomings", "A simple textbook formula does not capture these coupled degradation effects."),
        ("Role of Machine Learning", "Machine learning models can learn these complex nonlinear effects directly from test data."),
        ("Data Availability Dependency", "ML models can effectively learn corrections, but only if enough representative data is available.")
    ]
    add_bullets(s6, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s6_b2)
    set_note(s6, "The rule of mixtures is simple to compute, but it assumes ideal bonding between fibre and matrix, and perfectly aligned fibres. Real composites show effects such as voids and manufacturing variation, which a simple formula does not capture. Machine learning models can learn these effects from test data, but only if enough data is available.")

    # ==========================================
    # SLIDE 7: Why measured strength falls short (NEW)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Why Measured Strength Falls Short", "The Microstructural Gap [NEW]")
    add_footer(s7, 7)

    fig4_p = os.path.abspath("figures/fig4_why_strength_falls_short.png")
    if os.path.exists(fig4_p):
        s7.shapes.add_picture(fig4_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s7, "This slide explains the gap between the ideal estimate and measured strength. There are four main effects. Voids reduce the load-carrying area and can start cracks. Weak fibre-matrix bonding means the load is not fully passed from the matrix to the fibres. Fibre misalignment means some fibres carry less of the load. Manufacturing variation, such as changes in cure temperature and pressure, changes the final properties. Because of these effects, measured strength is usually below the ideal rule-of-mixtures value. The formula at the bottom of the slide ignores all of them, which is why we need a method that can also learn from data.")

    # ==========================================
    # SLIDE 8: Problem identification
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Problem Identification: Early-Stage Engineering Needs", "Industrial Bottleneck")
    add_footer(s8, 8)

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Physical Testing Limitations")
    s8_b1 = [
        ("Cost and Time Prohibitive", "Physical tensile testing of GFRP is expensive, slow, and destructive."),
        ("Poor Scalability", "Hard to scale across different fibre fractions, cure temperatures, and autoclave pressures."),
        ("Oversight of Analytical Tools", "Analytical estimates ignore many manufacturing effects and overpredict physical strength."),
        ("Coupled Variables", "Process variables (cure cycle, compaction pressure) interact nonlinearly with fiber fraction.")
    ]
    add_bullets(s8, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s8_b1)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Early Design Requirements")
    s8_b2 = [
        ("Early Strength Estimates", "Engineers need strength estimates early in the design process, before prototypes are built."),
        ("Fast Screening Tool", "What we need is a fast screening method that uses fibre volume fraction, cure temperature, and pressure together."),
        ("Minimizing Experimental Waste", "Accurate early screening narrows down the parameter space before costly physical coupon runs."),
        ("Multi-Parameter Synthesis", "Connecting constituent fractions and cure parameters in a unified framework.")
    ]
    add_bullets(s8, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s8_b2)
    set_note(s8, "Physical tensile testing of GFRP is expensive, slow, and hard to scale across different fibre fractions and cure conditions. Analytical estimates also ignore many manufacturing effects. Engineers need strength estimates early in the design process, before prototypes are built. What we need is a fast screening method that uses fibre volume fraction, cure temperature, and pressure together.")

    # ==========================================
    # SLIDE 9: Research gap
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Research Gap: Pure Physics vs. Pure Data", "Bridging Methodologies")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Limitations of Isolated Approaches")
    s9_b1 = [
        ("Rule-of-Mixtures Limitation", "The rule-of-mixtures estimate is based on physics, but it only works under idealized conditions."),
        ("Pure Data-Driven Limitation", "A purely data-driven model needs a massive volume of test data to train from scratch."),
        ("Risk of Physics Ignorance", "Purely empirical models may ignore known physics and produce physically unrealistic trends outside narrow bounds."),
        ("The Need for Synergy", "A standalone model fails to leverage the complementary strengths of analytical theory and empirical data.")
    ]
    add_bullets(s9, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s9_b1)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Our Combined Project Approach")
    s9_b2 = [
        ("Combining Both Approaches", "Our project combines the two: the rule-of-mixtures estimate becomes an input feature for the machine learning model."),
        ("Physics-Guided Baseline", "The analytical formula provides the initial scaling and physical foundation."),
        ("Data-Learned Correction", "Machine learning algorithms learn the defect and processing corrections from test data."),
        ("Improved Generalization", "Enables accurate predictions with fewer data samples while maintaining physical consistency.")
    ]
    add_bullets(s9, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s9_b2)
    set_note(s9, "The rule-of-mixtures estimate is based on physics, but it only works under idealised conditions. A purely data-driven model needs a lot of test data, and it may ignore known physics. Our project combines the two: the rule-of-mixtures estimate becomes an input feature for the machine learning model.")

    # ==========================================
    # SLIDE 10: Combining physics with machine learning (NEW)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Combining Physics with Machine Learning", "Model Architecture [NEW]")
    add_footer(s10, 10)

    fig5_p = os.path.abspath("figures/fig5_combining_physics_ml.png")
    if os.path.exists(fig5_p):
        s10.shapes.add_picture(fig5_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s10, "This diagram shows how the two approaches are combined. There are four inputs: fibre volume fraction, cure temperature, pressure, and the rule-of-mixtures estimate. The estimate is shown in a lighter box because it comes from physics rather than measurement. All four inputs feed the machine learning model, which can be linear regression, random forest, or gradient boosting. The output is the predicted tensile strength. The key point is that the model starts from the ideal value and learns the correction from test data.")

    # ==========================================
    # SLIDE 11: Objectives
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Project Objectives", "Goals & Targets")
    add_footer(s11, 11)

    objs = [
        ("Objective 1", "Tensile Strength Prediction", "Predict the tensile strength of E-glass and epoxy composite from fibre volume fraction, cure temperature, and pressure.", Inches(0.8), Inches(1.6)),
        ("Objective 2", "Physics-Informed Feature Engineering", "Use the analytical rule-of-mixtures estimate as an explicit input feature for machine learning models.", Inches(6.8), Inches(1.6)),
        ("Objective 3", "Multi-Model Comparison", "Compare three diverse ML algorithms: Linear Regression, Random Forest (300 trees), and Gradient Boosting.", Inches(0.8), Inches(4.3)),
        ("Objective 4", "Held-Out Statistical Evaluation", "Evaluate model accuracy and generalization on held-out test data using R², RMSE, and MAE metrics.", Inches(6.8), Inches(4.3))
    ]
    for tag, title, desc, l, t in objs:
        add_card(s11, l, t, Inches(5.7), Inches(2.4), title=f"{tag}: {title}")
        tb = s11.shapes.add_textbox(l + Inches(0.2), t + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK_GRAY

    set_note(s11, "We have four objectives. First, predict the tensile strength of E-glass and epoxy composite from fibre volume fraction, cure temperature, and pressure. Second, use the rule-of-mixtures estimate as an input feature. Third, compare linear regression, random forest, and gradient boosting. Fourth, evaluate the models on held-out data using R², RMSE, and MAE.")

    # ==========================================
    # SLIDE 12: Methodology
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Methodology: 5-Step Pipeline", "Workflow Execution")
    add_footer(s12, 12)

    steps = [
        ("Step 1", "Data Collection", "Collect data on fibre volume fraction (Vf), cure temperature (T), pressure (P), and strength."),
        ("Step 2", "Preprocessing", "Clean data, encode categories, handle missing values, and scale numerical ranges."),
        ("Step 3", "Feature Engineering", "Calculate and engineer the analytical rule-of-mixtures baseline estimate as an input."),
        ("Step 4", "Model Training", "Train three algorithms: Linear Regression, Random Forest (300 trees), and Gradient Boosting."),
        ("Step 5", "Evaluation", "Evaluate models on a held-out test set using R², RMSE, and MAE metrics.")
    ]
    w = Inches(2.18)
    gap = Inches(0.2)
    sx = Inches(0.8)
    for i, (tag, stitle, sdesc) in enumerate(steps):
        x = sx + i * (w + gap)
        add_card(s12, x, Inches(1.7), w, Inches(4.9), title=None)
        tb = s12.shapes.add_textbox(x + Inches(0.12), Inches(1.85), w - Inches(0.24), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = tag.upper()
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_BLUE

        p2 = tf.add_paragraph()
        p2.text = stitle
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_NAVY
        p2.space_before = Pt(4)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = sdesc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_DARK_GRAY

    set_note(s12, "Our pipeline has five steps, which I’ll go through from left to right. First, we collect data on fibre volume fraction, cure temperature, pressure, and strength. Second, we preprocess it by cleaning, encoding categories, and scaling the values. Third, we engineer features by adding the rule-of-mixtures estimate. Fourth, we train the three models. Fifth, we evaluate them on a held-out test set. The output is a predicted tensile strength for a given fibre volume fraction, cure temperature, and pressure.")

    # ==========================================
    # SLIDE 13: Materials and methods
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Materials & Analytical Methods", "Constituents & Formulation")
    add_footer(s13, 13)

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Material System Properties")
    s13_b1 = [
        ("E-Glass Fibre", "Typical virgin tensile strength of about 3400 MPa, modulus ~72.4 GPa, density 2.58 g/cm³."),
        ("Epoxy Matrix", "Typical cured neat resin tensile strength of about 70 MPa, modulus ~3.4 GPa, density 1.18 g/cm³."),
        ("Unidirectional Laminates", "Specimens are unidirectional (0° orientation), so rule of mixtures applies along fibre axis."),
        ("Handbook Values Check", "Handbook constituent strengths should be confirmed against supplier datasheets during experimental verification.")
    ]
    add_bullets(s13, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s13_b1)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Analytical Feature & Evaluation")
    s13_b2 = [
        ("Engineered Feature Formula", "sigma_c = sigma_f * Vf + sigma_m * (1 - Vf)."),
        ("Model Input Features", "Fibre volume fraction (Vf), cure temperature (T), consolidation pressure (P), and sigma_c."),
        ("Evaluation Metrics", "R² (coefficient of determination), RMSE (root mean squared error), and MAE (mean absolute error)."),
        ("Target Variable", "Ultimate longitudinal tensile strength of the cured composite coupon.")
    ]
    add_bullets(s13, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s13_b2)
    set_note(s13, "The material system is E-glass fibre with epoxy resin. The fibre has a typical tensile strength of about 3400 MPa, and the epoxy matrix about 70 MPa. The specimens are unidirectional, so the rule of mixtures applies along the fibre direction. The feature we use is sigma-c equals sigma-f times Vf, plus sigma-m times one minus Vf. The data consists of fibre volume fraction, cure temperature, pressure, and measured tensile strength. We evaluate the models with R², RMSE, and MAE. The handbook values for fibre and matrix strength should be checked against supplier datasheets, and we will say so when we present the results.")

    # ==========================================
    # SLIDE 14: Material specification
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Material Specification: Volume vs. Weight Fractions", "Constituent Details")
    add_footer(s14, 14)

    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Constituent Specifications")
    s14_b1 = [
        ("Fibre Reinforcement", "Unidirectional continuous E-glass with density rho_f = 2.58 g/cm³ and tensile strength ~3400 MPa."),
        ("Matrix Resin", "Bisphenol-A epoxy (DGEBA) cured with amine hardener, density rho_m = 1.18 g/cm³ and tensile strength ~70 MPa."),
        ("Resin Stoichiometry", "Cured at ~100:12 resin-to-hardener ratio by weight (typical value to be confirmed against datasheet)."),
        ("Studied Range", "Fibre volume fractions from 0.30 to 0.60, with 0.50 as the primary reference case.")
    ]
    add_bullets(s14, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s14_b1)

    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Weight Fraction Calculations")
    s14_b2 = [
        ("Conversion Formula", "Wf = (Vf * rho_f) / [Vf * rho_f + (1 - Vf) * rho_m]."),
        ("Vf = 0.30 Case", "Fibre weight fraction Wf = 48.4% by weight (composite density = 1.60 g/cm³)."),
        ("Vf = 0.50 Reference", "At volume fraction 0.50, fibres make up about 68.6% (~69%) of total composite weight."),
        ("Vf = 0.60 High Prepreg", "Fibre weight fraction Wf = 76.6% by weight (composite density = 2.02 g/cm³).")
    ]
    add_bullets(s14, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s14_b2)
    set_note(s14, "Here are the exact materials. The fibre is unidirectional E-glass with a density of about 2.58 grams per cubic centimetre and a tensile strength of about 3400 MPa. The matrix is a bisphenol-A epoxy, DGEBA, cured with an amine hardener at about a 100 to 12 resin-to-hardener ratio by weight. That ratio is a typical value and must be confirmed against the datasheet. We study fibre volume fractions from 0.30 to 0.60, with 0.50 as the reference case. The weight fractions on the slide are calculated from the densities shown. At a volume fraction of 0.5, the fibres make up about 69 percent of the weight.")

    # ==========================================
    # SLIDE 15: Unidirectional ply structure (NEW)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Unidirectional Ply Structure (Schematic)", "Microstructural Cross-Section [NEW]")
    add_footer(s15, 15)

    fig2_p = os.path.abspath("figures/fig2_ply_structure_schematic.png")
    if os.path.exists(fig2_p):
        s15.shapes.add_picture(fig2_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s15, "This is a schematic cross-section of a unidirectional ply at a fibre volume fraction of about 0.5. The blue circles are E-glass fibres, which carry most of the load. The shaded area is the epoxy matrix, which binds the fibres and transfers load between them. The fibres run into the page, so the load acts along their length. This is the direction in which the rule of mixtures applies. The drawing is not to scale.")

    # ==========================================
    # SLIDE 16: Fibre-matrix combination
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Fibre–Matrix Combination & Constituent Roles", "Load Distribution")
    add_footer(s16, 16)

    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Constituent Synergies")
    s16_b1 = [
        ("Fibre Reinforcement Role", "Glass fibres carry most of the tensile load (~98% of axial capacity)."),
        ("Polymer Matrix Role", "Epoxy matrix binds fibres together, transfers shear load between them, and protects against abrasion."),
        ("Combined Dependency", "Composite strength depends on constituent properties and how much of each constituent is present."),
        ("Interfacial Criticality", "Quality of stress transfer depends on chemical sizing and void-free consolidation.")
    ]
    add_bullets(s16, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s16_b1)

    add_card(s16, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Calculated Baseline & ML Role")
    s16_b2 = [
        ("Vf = 0.50 Ideal Capacity", "At fibre volume fraction 0.50, the ideal rule-of-mixtures value is about 1735 MPa."),
        ("Discrepancy with Reality", "Physical testing typically yields lower values due to fabrication defects."),
        ("ML Prediction Mission", "The machine learning model predicts combined strength from the three inputs (Vf, T, P)."),
        ("Nonlinear Correction", "Captures empirical trends without requiring complex manual correction factors.")
    ]
    add_bullets(s16, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s16_b2)
    set_note(s16, "This slide puts the constituents together. The fibre carries most of the load, and the matrix binds the fibres and transfers load between them. The composite’s strength depends on both materials and on how much of each is present. At a fibre volume fraction of 0.5, the ideal rule-of-mixtures value is about 1735 MPa. The machine learning model predicts the combined strength from the three inputs.")

    # ==========================================
    # SLIDE 17: Tensile behaviour of GFRP (NEW)
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Tensile Behaviour of GFRP (Schematic)", "Stress–Strain Mechanics [NEW]")
    add_footer(s17, 17)

    fig3_p = os.path.abspath("figures/fig3_stress_strain_schematic.png")
    if os.path.exists(fig3_p):
        s17.shapes.add_picture(fig3_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s17, "This is a schematic stress-strain curve. It shows the shape of the behaviour, not measured data, so no numbers appear on the axes. The curve starts with a linear elastic region, where stress rises in proportion to strain. It then ends in brittle fracture. Glass fibres fail with little plastic yield, so the curve drops sharply after the peak. The peak is the tensile strength, which is the value the model is trying to predict.")

    # ==========================================
    # SLIDE 18: Result and discussion
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Result & Discussion: Ideal Baseline vs. Simulation Check", "Analytical & ML Results")
    add_footer(s18, 18)

    fig1_p = os.path.abspath("figures/fig1_rom_ideal_curve.png")
    if os.path.exists(fig1_p):
        s18.shapes.add_picture(fig1_p, Inches(0.8), Inches(1.55), Inches(6.0), Inches(5.1))

    add_card(s18, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.1), title="Results Summary & Next Step")
    s18_b = [
        ("Ideal RoM Scaling", "The chart shows ideal RoM strength rising steadily with Vf: 403 MPa at 0.1 to 2068 MPa at 0.6 (ideal estimate, not measured data)."),
        ("Linear Regression Check", "Achieves an R² of 0.88 on synthetic test data, capturing the primary linear trend."),
        ("Random Forest Check", "Achieves an R² of 0.85 with 300 decision trees, capturing multi-variable interactions."),
        ("Gradient Boosting Check", "Achieves an R² of 0.84 on synthetic test data."),
        ("Rule of Mixtures Alone", "RoM alone yields R² of negative 0.90 because it ignores defects."),
        ("Synthetic Caveat", "These results are based on synthetic simulation data. The next step is to validate on physical laboratory tensile tests.")
    ]
    add_bullets(s18, Inches(7.2), Inches(2.2), Inches(5.1), Inches(4.3), s18_b, font_size=11.5)
    set_note(s18, "The chart shows the ideal rule-of-mixtures strength for E-glass and epoxy. It rises steadily with fibre volume fraction, from about 403 MPa at 0.1 to about 2068 MPa at 0.6. This is the ideal estimate, not measured data. The simulation check on synthetic data gives an R² of 0.88 for linear regression, 0.85 for random forest, and 0.84 for gradient boosting. The rule of mixtures alone gives negative 0.90. These are synthetic results. The next step is to replace the synthetic data with laboratory tensile tests.")

    # ==========================================
    # SLIDE 19: Dataset and simulation setup
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Dataset & Simulation Setup", "Synthetic Data Parameters")
    add_footer(s19, 19)

    add_card(s19, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Simulation Dataset Configuration")
    s19_b1 = [
        ("Sample Size & Split", "Generated 600 simulated E-glass and epoxy specimens and split them 80/20 (480 train / 120 test)."),
        ("Input Feature Ranges", "Vf from 0.30 to 0.60, cure temperature from 80 to 140 °C, pressure from 0.2 to 1.0 MPa."),
        ("Engineered Input", "Rule-of-mixtures ideal estimate included as an explicit fourth input feature."),
        ("Reproducible Setup", "Fixed random seed of 42 used for all data generation and model training splits.")
    ]
    add_bullets(s19, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s19_b1)

    add_card(s19, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Physical Degradation Mechanics & Caveat")
    s19_b2 = [
        ("Defect Degradation", "In simulation, strength is reduced by imperfect bonding and void content."),
        ("Experimental Noise", "Added 3 percent test scatter to emulate laboratory testing variation."),
        ("Machine Learning Algorithms", "Linear regression, random forest with 300 trees, and gradient boosting."),
        ("Synthetic Data Caveat", "All of this data is synthetic. It tests the pipeline, and it is not experimental evidence.")
    ]
    add_bullets(s19, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s19_b2)
    set_note(s19, "We generated 600 simulated E-glass and epoxy specimens and split them 80/20, giving 480 training samples and 120 test samples. The inputs are fibre volume fraction from 0.30 to 0.60, cure temperature from 80 to 140 degrees Celsius, pressure from 0.2 to 1.0 MPa, and the rule-of-mixtures estimate. The target is tensile strength. In the simulation, strength is reduced by imperfect bonding and voids, and then 3 percent test scatter is added. The models are linear regression, random forest with 300 trees, and gradient boosting, all with a fixed random seed of 42. All of this data is synthetic. It tests the pipeline, and it is not experimental evidence.")

    # ==========================================
    # SLIDE 20: Train–test workflow (NEW)
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Train–Test Workflow (Synthetic Data)", "Validation Strategy [NEW]")
    add_footer(s20, 20)

    fig6_p = os.path.abspath("figures/fig6_train_test_workflow.png")
    if os.path.exists(fig6_p):
        s20.shapes.add_picture(fig6_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s20, "This diagram shows how the data is used. The 600 samples are split 80/20. The 480 training samples fit the three models. The 120 test samples are held back and used only to score the fitted models on R², RMSE, and MAE. Each model is trained only on the training set, so the test scores give a fair check of how well it generalises.")

    # ==========================================
    # SLIDE 21: Simulation results (synthetic data)
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Simulation Results: Model Evaluation on Synthetic Test Data", "Held-Out Test Scores")
    add_footer(s21, 21)

    # Clean table layout on slide
    add_card(s21, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), title="Model Performance Comparison (Held-Out Test Set: N = 120)")

    # Insert PowerPoint Table
    table_shape = s21.shapes.add_table(5, 5, Inches(1.1), Inches(2.2), Inches(11.133), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(3.6)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(2.133)

    headers = ["Model Name", "R² Score", "RMSE (MPa)", "MAE (MPa)", "Model Category"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    data_rows = [
        ("Rule of Mixtures (Baseline)", "-0.898", "383.4", "362.9", "Analytical (No ML)"),
        ("Linear Regression", "0.879", "104.2", "82.5", "Physics-Informed ML"),
        ("Random Forest (300 trees)", "0.853", "114.6", "89.9", "Ensemble ML"),
        ("Gradient Boosting", "0.841", "118.2", "93.4", "Boosting Ensemble")
    ]
    for row_idx, row_vals in enumerate(data_rows, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_BG if row_idx % 2 == 1 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11.5)
            p.font.bold = (col_idx == 0 or col_idx == 1)
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(192, 0, 0) if val == "-0.898" else COLOR_DARK_GRAY

    # Explanatory text below table
    tb_exp = s21.shapes.add_textbox(Inches(1.1), Inches(5.1), Inches(11.133), Inches(1.4))
    tf_exp = tb_exp.text_frame
    tf_exp.word_wrap = True
    p_exp1 = tf_exp.paragraphs[0]
    p_exp1.text = "• The three ML models explain ~84% to 88% of variance in the synthetic test data, demonstrating successful error correction."
    p_exp1.font.name = FONT_FAMILY
    p_exp1.font.size = Pt(11)
    p_exp1.font.color.rgb = COLOR_NAVY
    p_exp1.font.bold = True

    p_exp2 = tf_exp.add_paragraph()
    p_exp2.text = "• Negative R² (-0.898) confirms RoM alone predicts worse than mean baseline because it ignores void and bonding knockdowns."
    p_exp2.font.name = FONT_FAMILY
    p_exp2.font.size = Pt(10.5)
    p_exp2.font.color.rgb = COLOR_DARK_GRAY

    set_note(s21, "This table gives the results row by row. The rule of mixtures alone has an R² of negative 0.898, an RMSE of 383.4 MPa, and an MAE of 362.9 MPa. Linear regression has an R² of 0.879, random forest 0.853, and gradient boosting 0.841. The three ML models explain about 84 to 88 percent of the variation in the synthetic test data. A negative R² means the rule of mixtures does worse than simply predicting the average, because it ignores bonding and void effects. This is a property of the synthetic data, and it must be checked with real measurements.")

    # ==========================================
    # SLIDE 22: Model comparison: R² on synthetic test data (NEW)
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Model Comparison: R² on Synthetic Test Data", "Performance Visualized [NEW]")
    add_footer(s22, 22)

    fig7_p = os.path.abspath("figures/fig7_model_comparison_r2.png")
    if os.path.exists(fig7_p):
        s22.shapes.add_picture(fig7_p, Inches(0.8), Inches(1.55), Inches(6.8), Inches(5.1))

    add_card(s22, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.1), title="Model Performance Insights")
    s22_b = [
        ("Baseline Gap", "The grey bar shows Rule of Mixtures on its own, falling well below zero (R² = -0.898) due to uncalibrated overprediction."),
        ("Close ML Cluster", "The three machine learning models sit close together, between 0.84 and 0.88."),
        ("No Dramatic Divergence", "Differences between ML algorithms are small (84% to 88%), so simulation data does not clearly favour one algorithm over another."),
        ("Linear Regression Strength", "Linear regression performs slightly better because the primary volume fraction scaling is fundamentally linear."),
        ("Synthetic Data Note", "Again, these results use synthetic data and test the pipeline's computational feasibility.")
    ]
    add_bullets(s22, Inches(8.0), Inches(2.2), Inches(4.3), Inches(4.3), s22_b, font_size=11)
    set_note(s22, "This bar chart shows the same R² values as the table. The grey bar is the rule of mixtures on its own, which falls well below zero. The three machine learning models sit close together, between 0.84 and 0.88. The differences between them are small, so the simulation does not clearly favour one model. Again, these results use synthetic data.")

    # ==========================================
    # SLIDE 23: Predicted vs actual strength
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Predicted vs. Actual Strength on Held-Out Test Data", "Model Goodness-of-Fit")
    add_footer(s23, 23)

    fig8_p = os.path.abspath("figures/fig8_predicted_vs_actual.png")
    if os.path.exists(fig8_p):
        s23.shapes.add_picture(fig8_p, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    set_note(s23, "Each point on these plots is one test sample. The horizontal axis shows the actual strength, and the vertical axis shows the predicted strength. The dashed line is where predictions equal actual values. The tighter the points sit around that line, the better the model. There is one plot for each of the three models. All of these points come from synthetic data.")

    # ==========================================
    # SLIDE 24: Limitations and future work
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Limitations & Future Work", "Critical Self-Assessment")
    add_footer(s24, 24)

    add_card(s24, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Current Study Limitations")
    s24_b1 = [
        ("Idealized RoM Physics", "The rule of mixtures assumes ideal bonding and perfectly aligned fibres."),
        ("Data Quality Dependency", "Model accuracy depends directly on the size, distribution, and quality of the test data."),
        ("Extrapolation Risk", "Predictions become less reliable outside the training range (e.g., Vf > 0.65 or non-standard cures)."),
        ("Interpretability Trade-offs", "Tree-based and boosting models are harder to interpret mechanically than a transparent equation.")
    ]
    add_bullets(s24, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s24_b1)

    add_card(s24, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Proposed Future Research")
    s24_b2 = [
        ("Physical Test Campaign", "Collect real laboratory GFRP tensile tests across fibre fractions, cure cycles, and pressures."),
        ("Additional Microstructural Features", "Add fibre diameter, interface shear quality, and measured void content to feature sets."),
        ("Interpretable Hybrid Models", "Develop hybrid models that directly combine physics equations with ML correction terms."),
        ("Laminate Validation", "Validate strength predictions on newly fabricated GFRP laminates before design adoption.")
    ]
    add_bullets(s24, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s24_b2)
    set_note(s24, "We want to be upfront about the limitations. The rule of mixtures assumes ideal bonding and aligned fibres. Model accuracy depends on the size and quality of the test data. Predictions are less reliable outside the training range. Tree-based and boosting models are also harder to interpret than a simple formula. For future work, we plan to collect more GFRP tests across fibre fractions, cure cycles, and pressures. We also want to add fibre diameter, interface quality, and void content. Another direction is a hybrid model that combines physics equations with machine learning and is easier to interpret. Finally, we will validate predictions on new GFRP laminates.")

    # ==========================================
    # SLIDE 25: Conclusion
    # ==========================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Conclusions & Key Takeaways", "Summary of Work")
    add_footer(s25, 25)

    add_card(s25, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Project Conclusions")
    s25_b1 = [
        ("Physics-Based Baseline", "The rule of mixtures provides an indispensable physics-based baseline for GFRP strength."),
        ("Machine Learning Addition", "Machine learning adds the secondary defect and cure effects that the baseline misses, using test data."),
        ("Combined Screening Power", "Together they support faster and cheaper strength screening for new GFRP component designs."),
        ("Demonstrated Workflow", "The pipeline establishes feasibility for integrating domain physics with predictive ML.")
    ]
    add_bullets(s25, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s25_b1)

    add_card(s25, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Practical Engineering Guidance")
    s25_b2 = [
        ("Mandatory Physical Validation", "Validate on measured GFRP laminates before final design use."),
        ("Early Concept Sizing", "Use physics-informed predictions to narrow candidate material fractions during trade studies."),
        ("Defect Mitigation", "Maintain strict cure cycle and compaction pressure controls to minimize void formation."),
        ("Transparent Modeling", "Always benchmark ML predictions against the classical physical upper bound.")
    ]
    add_bullets(s25, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s25_b2)
    set_note(s25, "To summarise: the rule of mixtures gives a physics-based baseline for GFRP strength. Machine learning adds the effects that the baseline misses, using test data. Together they support faster and cheaper strength screening for new GFRP designs. Before using the model for design decisions, we need to validate it on measured GFRP laminates.")

    # ==========================================
    # SLIDE 26: Publication and work in progress
    # ==========================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "Publication & Work in Progress", "Project Milestones")
    add_footer(s26, 26)

    add_card(s26, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Completed Project Milestones")
    s26_b1 = [
        ("Data Pipeline Architecture", "Synthetic data collection pipeline with 600 specimens completed and validated."),
        ("Feature Engineering", "Integrated analytical rule-of-mixtures baseline as an engineered physics feature."),
        ("Model Development", "Implemented, trained, and tuned Linear Regression, Random Forest, and Gradient Boosting."),
        ("Held-Out Evaluation", "Full statistical evaluation completed on 120 held-out test samples with R², RMSE, and MAE.")
    ]
    add_bullets(s26, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s26_b1)

    add_card(s26, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Current Tasks & Publication Plans")
    s26_b2 = [
        ("Literature Review Expansion", "The full literature table, reviewing 30+ peer-reviewed articles, is being finalized."),
        ("Experimental Testing Plan", "Formulating laboratory coupon testing campaign following ASTM D3039 procedures."),
        ("Publication Planning", "The conference/journal publication plan is currently being confirmed by the team."),
        ("Repository & Dashboard", "Open-source Python simulation dashboard and documentation prepared.")
    ]
    add_bullets(s26, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s26_b2)
    set_note(s26, "Our current work covers data collection and preprocessing, model training, and evaluation. The publication plan is still to be confirmed by the team.")

    # ==========================================
    # SLIDE 27: References
    # ==========================================
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "References & Literature Foundations", "Academic Citations")
    add_footer(s27, 27)

    add_card(s27, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Foundational Composite Treatises")
    s27_b1 = [
        ("Jones, R. M. (1999)", "Mechanics of Composite Materials, 2nd Edition, Taylor & Francis / CRC Press. ISBN: 978-1560327127."),
        ("Hull, D. & Clyne, T. W. (1996)", "An Introduction to Composite Materials, 2nd Edition, Cambridge University Press. ISBN: 978-0521388559."),
        ("Daniel, I. M. & Ishai, O. (2006)", "Engineering Mechanics of Composite Materials, 2nd Edition, Oxford University Press. ISBN: 978-0195150971."),
        ("Mallick, P. K. (2007)", "Fiber-Reinforced Composites: Materials, Manufacturing, and Design, 3rd Edition, CRC Press. ISBN: 978-0849342059.")
    ]
    add_bullets(s27, Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3), s27_b1)

    add_card(s27, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), title="Standards & Ongoing Review")
    s27_b2 = [
        ("ASTM D3039/D3039M-17", "Standard Test Method for Tensile Properties of Polymer Matrix Composite Materials, ASTM International."),
        ("ASTM D3171-15", "Standard Test Methods for Constituent Content of Composite Materials (Resin Burn-off), ASTM International."),
        ("Soden, P. D. et al. (1998)", "Worldwide Failure Exercise (WWFE-I) Lamina Properties, Composites Science and Technology."),
        ("Full Literature List", "The full literature list with thirty research articles will be added as the team completes the review.")
    ]
    add_bullets(s27, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3), s27_b2)
    set_note(s27, "Our main references are R. M. Jones, Mechanics of Composite Materials, and D. Hull and T. W. Clyne, An Introduction to Composite Materials. The full literature list will be added as the team completes the review. Thank you. We’re happy to take questions.")

    prs.save(output_filename)
    print(f"Presentation successfully created and saved to {output_filename} with {len(prs.slides)} slides.")


if __name__ == "__main__":
    build_expanded_deck()

