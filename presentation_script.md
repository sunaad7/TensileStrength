# Presentation Script

## Predicting Tensile Strength of E-glass Fibre/Epoxy Composite (GFRP) Using Machine Learning and the Rule of Mixtures

**Estimated running time:** about 25 to 30 minutes, plus questions.  
*Note: Replace `[Name]` with the presenting team members’ names. Slides marked **(NEW)** were added to expand the deck to 27 slides.*

---

### Slide 1: Title
Good morning, everyone. My name is [Name], and with me are [Name] and [Name]. Our project is about predicting the tensile strength of E-glass fibre and epoxy composites, also called GFRP, using machine learning and the rule of mixtures. This work was done for our Fundamentals of Composite Materials course.

---

### Slide 2: Table of Contents
Here is the outline. I will start with the problem and the literature, then explain our method and materials. After that, we will look at the results, which are based on simulated data, and finish with the limitations, the conclusion, and our references.

---

### Slide 3: Introduction
E-glass fibre and epoxy composite, or GFRP, combines strong glass fibres with an epoxy matrix. The result is a material with a high strength-to-weight ratio, which is why engineers use it.

The problem is that measuring its tensile strength through physical testing is expensive and time-consuming. The rule of mixtures gives a quick estimate from the fibre volume fraction and the properties of each constituent, but it is a simple formula.

Our project studies unidirectional E-glass and epoxy, and uses machine learning to predict tensile strength from three inputs: fibre volume fraction, cure temperature, and pressure.

---

### Slide 4: Application
GFRP is used in several areas. In aerospace, lightweight panels and fairings help reduce fuel use, because every gram saved matters. In automotive, it is used for lightweight body panels and parts. Structural uses include load-bearing parts with low self-weight, such as pipes and tanks.

We have also added sporting goods and wind turbine blades. In both, stiffness and low weight are important, so the same material choice applies.

---

### Slide 5: Literature review
Analytical models such as the rule of mixtures estimate composite strength from the properties of the constituents, and our references cover them. Experimental tensile testing gives accurate values, but every new combination of materials and conditions has to be tested separately. That is the main reason we want a faster method. The full literature table, with at least thirty research articles, is still being completed by the team.

---

### Slide 6: Findings from literature
The rule of mixtures is simple to compute, but it assumes ideal bonding between fibre and matrix, and perfectly aligned fibres. Real composites show effects such as voids and manufacturing variation, which a simple formula does not capture. Machine learning models can learn these effects from test data, but only if enough data is available.

---

### Slide 7: Why measured strength falls short (NEW)
This slide explains the gap between the ideal estimate and measured strength. There are four main effects. Voids reduce the load-carrying area and can start cracks. Weak fibre-matrix bonding means the load is not fully passed from the matrix to the fibres. Fibre misalignment means some fibres carry less of the load. Manufacturing variation, such as changes in cure temperature and pressure, changes the final properties.

Because of these effects, measured strength is usually below the ideal rule-of-mixtures value. The formula at the bottom of the slide ignores all of them, which is why we need a method that can also learn from data.

---

### Slide 8: Problem identification
Physical tensile testing of GFRP is expensive, slow, and hard to scale across different fibre fractions and cure conditions. Analytical estimates also ignore many manufacturing effects. Engineers need strength estimates early in the design process, before prototypes are built. What we need is a fast screening method that uses fibre volume fraction, cure temperature, and pressure together.

---

### Slide 9: Research gap
The rule-of-mixtures estimate is based on physics, but it only works under idealised conditions. A purely data-driven model needs a lot of test data, and it may ignore known physics. Our project combines the two: the rule-of-mixtures estimate becomes an input feature for the machine learning model.

---

### Slide 10: Combining physics with machine learning (NEW)
This diagram shows how the two approaches are combined. There are four inputs: fibre volume fraction, cure temperature, pressure, and the rule-of-mixtures estimate. The estimate is shown in a lighter box because it comes from physics rather than measurement. All four inputs feed the machine learning model, which can be linear regression, random forest, or gradient boosting. The output is the predicted tensile strength.

The key point is that the model starts from the ideal value and learns the correction from test data.

---

### Slide 11: Objectives
We have four objectives. First, predict the tensile strength of E-glass and epoxy composite from fibre volume fraction, cure temperature, and pressure. Second, use the rule-of-mixtures estimate as an input feature. Third, compare linear regression, random forest, and gradient boosting. Fourth, evaluate the models on held-out data using R², RMSE, and MAE.

---

### Slide 12: Methodology
Our pipeline has five steps, which I’ll go through from left to right. First, we collect data on fibre volume fraction, cure temperature, pressure, and strength. Second, we preprocess it by cleaning, encoding categories, and scaling the values. Third, we engineer features by adding the rule-of-mixtures estimate. Fourth, we train the three models. Fifth, we evaluate them on a held-out test set. The output is a predicted tensile strength for a given fibre volume fraction, cure temperature, and pressure.

---

### Slide 13: Materials and methods
The material system is E-glass fibre with epoxy resin. The fibre has a typical tensile strength of about 3400 MPa, and the epoxy matrix about 70 MPa. The specimens are unidirectional, so the rule of mixtures applies along the fibre direction.

The feature we use is sigma-c equals sigma-f times Vf, plus sigma-m times one minus Vf. The data consists of fibre volume fraction, cure temperature, pressure, and measured tensile strength. We evaluate the models with R², RMSE, and MAE. The handbook values for fibre and matrix strength should be checked against supplier datasheets, and we will say so when we present the results.

---

### Slide 14: Material specification
Here are the exact materials. The fibre is unidirectional E-glass with a density of about 2.58 grams per cubic centimetre and a tensile strength of about 3400 MPa. The matrix is a bisphenol-A epoxy, DGEBA, cured with an amine hardener at about a 100 to 12 resin-to-hardener ratio by weight. That ratio is a typical value and must be confirmed against the datasheet.

We study fibre volume fractions from 0.30 to 0.60, with 0.50 as the reference case. The weight fractions on the slide are calculated from the densities shown. At a volume fraction of 0.5, the fibres make up about 69 percent of the weight.

---

### Slide 15: Unidirectional ply structure (NEW)
This is a schematic cross-section of a unidirectional ply at a fibre volume fraction of about 0.5. The blue circles are E-glass fibres, which carry most of the load. The shaded area is the epoxy matrix, which binds the fibres and transfers load between them.

The fibres run into the page, so the load acts along their length. This is the direction in which the rule of mixtures applies. The drawing is not to scale.

---

### Slide 16: Fibre-matrix combination
This slide puts the constituents together. The fibre carries most of the load, and the matrix binds the fibres and transfers load between them. The composite’s strength depends on both materials and on how much of each is present. At a fibre volume fraction of 0.5, the ideal rule-of-mixtures value is about 1735 MPa. The machine learning model predicts the combined strength from the three inputs.

---

### Slide 17: Tensile behaviour of GFRP (NEW)
This is a schematic stress-strain curve. It shows the shape of the behaviour, not measured data, so no numbers appear on the axes.

The curve starts with a linear elastic region, where stress rises in proportion to strain. It then ends in brittle fracture. Glass fibres fail with little plastic yield, so the curve drops sharply after the peak. The peak is the tensile strength, which is the value the model is trying to predict.

---

### Slide 18: Result and discussion
The chart shows the ideal rule-of-mixtures strength for E-glass and epoxy. It rises steadily with fibre volume fraction, from about 403 MPa at 0.1 to about 2068 MPa at 0.6. This is the ideal estimate, not measured data.

The simulation check on synthetic data gives an R² of 0.88 for linear regression, 0.85 for random forest, and 0.84 for gradient boosting. The rule of mixtures alone gives negative 0.90. These are synthetic results. The next step is to replace the synthetic data with laboratory tensile tests.

---

### Slide 19: Dataset and simulation setup
We generated 600 simulated E-glass and epoxy specimens and split them 80/20, giving 480 training samples and 120 test samples. The inputs are fibre volume fraction from 0.30 to 0.60, cure temperature from 80 to 140 degrees Celsius, pressure from 0.2 to 1.0 MPa, and the rule-of-mixtures estimate.

The target is tensile strength. In the simulation, strength is reduced by imperfect bonding and voids, and then 3 percent test scatter is added. The models are linear regression, random forest with 300 trees, and gradient boosting, all with a fixed random seed of 42.

All of this data is synthetic. It tests the pipeline, and it is not experimental evidence.

---

### Slide 20: Train-test workflow (NEW)
This diagram shows how the data is used. The 600 samples are split 80/20. The 480 training samples fit the three models. The 120 test samples are held back and used only to score the fitted models on R², RMSE, and MAE. Each model is trained only on the training set, so the test scores give a fair check of how well it generalises.

---

### Slide 21: Simulation results (synthetic data)
This table gives the results row by row. The rule of mixtures alone has an R² of negative 0.898, an RMSE of 383.4 MPa, and an MAE of 362.9 MPa. Linear regression has an R² of 0.879, random forest 0.853, and gradient boosting 0.841.

The three ML models explain about 84 to 88 percent of the variation in the synthetic test data. A negative R² means the rule of mixtures does worse than simply predicting the average, because it ignores bonding and void effects. This is a property of the synthetic data, and it must be checked with real measurements.

---

### Slide 22: Model comparison: R² on synthetic test data (NEW)
This bar chart shows the same R² values as the table. The grey bar is the rule of mixtures on its own, which falls well below zero. The three machine learning models sit close together, between 0.84 and 0.88. The differences between them are small, so the simulation does not clearly favour one model. Again, these results use synthetic data.

---

### Slide 23: Predicted vs actual strength
Each point on these plots is one test sample. The horizontal axis shows the actual strength, and the vertical axis shows the predicted strength. The dashed line is where predictions equal actual values. The tighter the points sit around that line, the better the model. There is one plot for each of the three models. All of these points come from synthetic data.

---

### Slide 24: Limitations and future work
We want to be upfront about the limitations. The rule of mixtures assumes ideal bonding and aligned fibres. Model accuracy depends on the size and quality of the test data. Predictions are less reliable outside the training range. Tree-based and boosting models are also harder to interpret than a simple formula.

For future work, we plan to collect more GFRP tests across fibre fractions, cure cycles, and pressures. We also want to add fibre diameter, interface quality, and void content. Another direction is a hybrid model that combines physics equations with machine learning and is easier to interpret. Finally, we will validate predictions on new GFRP laminates.

---

### Slide 25: Conclusion
To summarise: the rule of mixtures gives a physics-based baseline for GFRP strength. Machine learning adds the effects that the baseline misses, using test data. Together they support faster and cheaper strength screening for new GFRP designs. Before using the model for design decisions, we need to validate it on measured GFRP laminates.

---

### Slide 26: Publication and work in progress
Our current work covers data collection and preprocessing, model training, and evaluation. The publication plan is still to be confirmed by the team.

---

### Slide 27: References
Our main references are R. M. Jones, Mechanics of Composite Materials, and D. Hull and T. W. Clyne, An Introduction to Composite Materials. The full literature list will be added as the team completes the review.

Thank you. We’re happy to take questions.

---

### Likely Questions and Short Answers

**Q1: Are the results from real tests?**  
*Answer:* No. The R² and error values come from simulated data built to test the pipeline. Laboratory tensile tests are the next step.

**Q2: Why is the rule of mixtures’ R² negative?**  
*Answer:* On this synthetic data, the formula ignores bonding and void effects, so it predicts worse than the average. This is a property of the simulation and must be re-checked with real measurements.

**Q3: Why use three models?**  
*Answer:* Linear regression is simple and easy to interpret. Random forest and gradient boosting can capture more complex patterns, so comparing them shows whether the extra complexity helps.

**Q4: Where do the handbook values come from?**  
*Answer:* The fibre and matrix strengths are typical values. We will confirm them against supplier datasheets before using the model for design.

