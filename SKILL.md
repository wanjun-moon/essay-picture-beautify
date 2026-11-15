---
name: essay-picture-beautify
description: Research-paper figure refinement grounded in the manuscript, captions, equations, underlying data and visual semantics. Redraw diagrams, plot authentic results, assemble comparison panels, and validate scientific fidelity and export quality.
---

# Research Figure Beautification

## Objective
Produce publication-ready scientific figures with improved readability, visual hierarchy, typography and consistency **without changing the scientific claims or measurement information**. Read the paper and figure caption before editing. Scientific semantics take priority over visual aesthetics.

## Intake and contextual analysis
1. Collect the paper, figure identifiers, caption, editable source, data, image assets, target journal, page/column widths and desired formats. Identify whether the requested operation is cosmetic layout, precise data-driven replotting, or genuine figure reconstruction.
2. Extract and inspect target pages and their neighbors, locate every text reference to each figure, read associated equations, experiments, limitations and appendices. Use `scripts/inspect_paper.py` as an initial guide, then visually inspect original pages at readable resolution.
3. For each figure, create an internal semantic inventory: panel label, purpose, scientific claim, source provenance, node/arrow meaning, coordinate and color semantics, numerical values and uncertainty, conditions, symbols, exact text, and non-negotiable details.
4. Establish what may be modified. Safe typical changes: spacing, alignment, fonts, border treatments, decorative backgrounds, legend positions and consistent palettes. Changes to data, methods, images or scientific relationships require validated original source material.

## Figure-type routing
Consult `references/figure_types.md` for 14 figure types and `references/design_system.md` for style decisions.
- **Computational methods / neural architectures:** Preserve directed edges, branch joins, operators, label-space mappings, training/inference boundaries, parameters, model freezing, weight sharing and temporal order. Keep symbols identical to the manuscript.
- **Line, bar, scatter and quantitative plots:** Recreate from the author's numeric data. Keep units, categorical ordering, grouping, limits, error bars, confidence level, sample sizes, baselines and statistical procedures. Never invent data from visual appearance. See `scripts/plot_results.py`.
- **Medical, microscopy, remote sensing and other image comparison panels:** Preserve original pixel content and relevant display parameters. Use the same source scene and registered crop for corresponding methods. Never hallucinate missing anatomy or imply synthetic results are observed outputs. See `scripts/compose_panels.py`.
- **Prompt, code, UI or questionnaire figures:** Keep literal strings, conditionals, field names and states exact. Improve containers and typography only.
- **Maps / heatmaps / matrices:** Preserve direction of scales, missing-data indicators, normalization, populations, colorbar endpoints, bin boundaries and spatial orientation.
- **Statistical/causal models:** Preserve directed assumptions, coefficients, standard errors, significance marks and variable names; do not change interpreted causal direction.

## Visual hierarchy and figure language
1. Group information by scientific role. Use natural reading order. Make the principal scientific pathway prominent; supporting details remain legible at final publication width.
2. Use a restrained consistent palette, preferably color-vision-accessible. Color is redundant with labels, dashes, shapes or other encodings for essential distinctions.
3. Choose matching typography and mathematical notation. Avoid extremely small labels. For raster imagery, put explanatory text on separate vector layers when possible.
4. Use whitespace for grouping. Avoid gratuitous shadows, gradients, neon borders, decorative icons, 3-D effects or low-contrast pastel-on-pastel text.
5. Distinguish descriptive grouping borders from actual computational operators; avoid arrows that imply non-existent supervision or information flow.
6. Keep multiple figures consistent in color-to-method mapping, line styles, panel labels, icons, text sizes and exports.

## Personalized optimization from the user's research materials

When the user explicitly authorizes it, use the selected project papers, original figures, numeric datasets, plotting sources, journal templates and approved visual references to infer a project-specific visual style. Keep scientific facts and visual preferences separate: source data and manuscript content govern values and relationships; user feedback governs presentation parameters only.

Use `references/personalized_optimization.md` for the full procedure. In brief:
1. Inspect only files selected by the user; do not scan unrelated folders or accounts.
2. Infer provisional visual settings from approved examples and the target journal.
3. Generate a figure preview and disclose the settings used.
4. Record explicit accept/reject feedback. Silence is not approval.
5. With permission, aggregate feedback by figure type using `scripts/learn_style_profile.py` and a user-selected local JSONL log/profile path.
6. Apply learned preferences only when there is sufficient support. Journal rules, accessibility, readability and scientific fidelity take priority.
7. Let the user inspect, edit, export or delete the profile and feedback log.

This feature performs local preference learning and visual-parameter calibration. It does not fine-tune model weights or train a shared model. Never place raw manuscripts, images, patient identifiers, unpublished measurements or credentials in the feedback log, and never transmit project materials by default. If profile creation is not approved, complete the current task without retaining preferences.

## Production and exports
- Prefer editable SVG/PDF for diagrams and graphs. Save underlying code/data when plotting. Embed original raster imagery without lossy resampling or modification when pixel fidelity matters.
- Default deliverables: an editable source, press-ready PDF/SVG, PNG preview, and a concise figure-specific verification note. Use journal artwork guidance when provided; otherwise verify physical width, final-size text, color mode requirements and effective DPI.
- `scripts/plot_results.py` supports CSV line charts and point-plus-interval plots; `scripts/compose_panels.py` creates pixel-preserving SVG composite layouts; `scripts/inspect_paper.py` inventories PDF figures and captions.

## Required validation
1. Open/render output at its final physical size; visually inspect panel order, spacing, legends, equations and symbol integrity.
2. Compare every panel against source data and manuscript semantics. For plots, independently verify axis values, uncertainties and rankings. For images, check source hashes/crop coordinates and registration. For diagrams, check nodes, connectors and arrow direction.
3. Confirm figure-caption agreement and journal requirements. Check fonts, output dimensions, SVG validity and PDF display. Repeat editing and verification until the figure is correct.
4. Do not claim exact data, preserved pixels, font embedding, or successful technical tests unless verified. Do not silently create new experimental results.

## References
- `references/figure_types.md`: taxonomy and rules for 14 figure types.
- `references/design_system.md`: scientific drawing and export standards.
- `references/paper_index.csv`: index of supplied research articles (titles inferred from supplied filenames; not a substitute for paper review).
- `references/case_studies.md`: anchored examples of figure/body relationships from the supplied papers.
- `references/personalized_optimization.md`: opt-in local preference learning, privacy and feedback workflow.
- `scripts/learn_style_profile.py`: builds a local style profile from explicit accept/reject feedback.
