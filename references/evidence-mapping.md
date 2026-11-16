# Match figure design to evidence

Choose a figure's visual form from the research question and evidence, not from the discipline name alone. Check the target figure, caption, referring passages, methods and available source data. Research articles, reviews and conceptual proposals have different evidence boundaries. When a manuscript and caption disagree, preserve the discrepancy as unresolved; do not silently pick a version.

## Build a panel-to-claim map

For each panel, record its role, evidence source, population or sample, conditions, variables and units, encodings, comparison, uncertainty definition and textual claim. Identify what the source actually supports and whether the panel is an illustration, experimental measurement, simulation, model prediction, proposed explanation, or review synthesis. A representative photograph, selected example or qualitative capability chart is not a population-level statistic. A theory or simulation of human behavior is not a human-subject experiment.

Connect workflow stages to the actual methods: inputs and outputs, controlled and changing conditions, branch and arrow semantics, pretraining versus fine-tuning, frozen versus trainable modules, supervision, reference and test sets. Label manual intervention, hardware and computational boundaries when they affect the conclusion. Separate measured or reconstructed results from hypothesized mechanisms and future uses.

## Quantitative and visual fidelity

- Preserve axes and units, scales and transformations, zero or broken axes, negative signs, baseline, category order, data windows and colorbars. Explain whether connecting lines join categories or represent continuous values.
- Identify the experimental unit and denominator: patients, biological or technical replicates, seeds, images, grid points, events and bootstrap resamples are not interchangeable. Keep confidence intervals, standard deviations, ranges, percentiles and systematic variations distinct. State paired designs, confidence level, multiple comparisons and statistical test where material.
- Match metrics and thresholds to each panel: top-1 versus top-k, trajectory versus field error, relative versus absolute error, per-sample versus pooled quantities, nominal versus perturbed conditions. Keep training, calibration and postprocessing costs in their actual measurement scope.
- Do not derive exact results from a screenshot or invent missing values. Preserve source-image content and aligned comparisons; differentiate image scale bars and representative images from quantitative replicates. For a proposed reconstruction without source data, label limitations and do not imply validated results.
- Compare plots and text at final size, including symbols, minus signs and clipping. Check source-data values and conditions when available; record unverified quantities explicitly.

## Domain-sensitive examples from inspected papers

- Fluid mechanics: Wan et al., DOI 10.1038/s42256-026-01316-7, Figs. 1–5 and Extended Data 3. Connect trajectory and velocity constraints to each test configuration; show reference, prediction and error with correct time and color scales. Distinguish simulated flow from in-vitro circulation, and pressure prediction uncertainty from independent pressure accuracy.
- Particle physics: Hsu et al., DOI 10.1038/s42256-026-01322-9, Figs. 1–5. Separate pretraining from downstream heads and costs; pair mass scans with signal/background assumptions. Distinguish simulated search benchmarks from rediscovery of a known resonance in experimental open data, and statistical error bars from systematic-variation bands.
- Robotics: Saikot et al., DOI 10.1038/s42256-026-01335-4, Figs. 1–6. Pair hardware and force characterization with a configuration-transition schematic and photographs of the corresponding task. Do not translate a qualitative capability map into a numeric benchmark, or teleoperated demonstrations into autonomous planning. State the number of trials and whether whiskers are ranges.
- Materials modeling: Li et al., DOI 10.1038/s42256-026-01326-5, Figs. 1–5. Pair atomic structures and predicted bands with their numerical reference, state the evaluated energy window and show the distribution beyond selected examples. Timing for one pipeline stage is not full end-to-end speedup.
- Molecular structure prediction: Yao et al., DOI 10.1038/s43588-026-01062-1, Figs. 1–6. Describe assembly and symmetry assumptions; compare full and partial complexes and preserve the target-wise examples where a competing method performs better. Distinguish the scores, thresholds and unavailable comparator outputs.
- Dynamic networks: Zhang et al., DOI 10.1038/s43588-026-01068-9, Figs. 1–5. Pair the interaction/update/switching process with the network topology and model assumptions. Distinguish a representative simulated trajectory from a statistical ensemble; for reciprocal thresholds retain the sign and direction of favorable change.

These are examples of evidence mapping, not universal figure templates or independent validation of the cited studies. Source publications and images may have reuse restrictions; don't redistribute paper images without appropriate rights.
