# Personalized Figure-Style Optimization

## Purpose

Adapt figure presentation to a user's research context and repeatedly expressed preferences. The feature uses the user's own project materials as contextual reference and explicit accept/reject feedback to refine a local style profile.

**Meaning of “training” in this skill:** this is local preference learning and parameter calibration. It does not fine-tune model weights, train a foundation model, or send project materials to an external training service. Do not describe it as neural-network training.

## Inputs and permitted use

Use only materials the user has supplied or explicitly selected for this task:

- manuscript PDFs, figure captions, equations and supplementary material, to understand scientific semantics;
- original figure files, vector sources, plotting scripts and numeric datasets, to reproduce the user's actual research;
- user-approved reference figures and journal templates, to infer typography, spacing, palette and panel conventions;
- explicit feedback on generated versions, such as accept, reject, or a requested correction.

Separate scientific content from visual preference. Numeric datasets and manuscript equations determine scientific values and relationships. Feedback may tune visual parameters, never alter scientific values, methods, labels, statistical conclusions, or source-image content.

## Runtime workflow

1. **Ask/confirm scope when needed.** At first use, state which project files will be inspected and whether the user wants a reusable local style profile. Do not scan unrelated folders or connected accounts automatically.
2. **Build a project context.** Read the selected paper and figure references. Identify figure types, discipline-specific conventions, journal requirements, fonts available, and existing palette/line conventions.
3. **Infer candidate visual settings.** Derive candidate palette, font family/size, line width, marker size, panel layout, legend placement, spacing, background, axis and annotation style from approved examples. Mark inferred values as provisional.
4. **Generate a first figure.** Preserve source data and scientific semantics. Present a preview and list the visual settings used.
5. **Collect explicit feedback.** Record only direct accept/reject decisions or explicit corrections. Do not infer approval from silence, continued use, or unrelated comments. A correction should be recorded as rejection of the old attribute and acceptance of the replacement only when the user clearly approves it.
6. **Update the local profile.** Append one JSONL record per feedback event. Run `scripts/learn_style_profile.py` to aggregate accepted and rejected choices by figure type. Use a minimum support of two by default to avoid overfitting to one example.
7. **Apply conservatively.** On later figures, apply learned preferences only when the figure type matches and the evidence is sufficient. Journal requirements, accessibility, legibility, and scientific correctness take precedence. If learned preferences conflict with one another or with a journal specification, show the conflict and choose the compliant setting.
8. **Verify each result.** Re-check data, captions, dimensions, text readability, source-image fidelity and export. A style profile never replaces figure-specific validation.
9. **Allow correction and reset.** Let the user inspect, edit, export or delete the profile and feedback log. Never overwrite the only copy; write a new profile atomically or retain a backup.

## Feedback format

Each line in the feedback JSONL file is one explicit decision:

```json
{"figure_type":"method_diagram","rating":"accept","attributes":{"palette":"blue_orange","font_family":"Arial","layout":"left_to_right","line_width":"1.2pt"}}
{"figure_type":"quantitative_plot","rating":"reject","attributes":{"palette":"rainbow","legend_position":"inside_upper_right"}}
```

Supported attributes are intentionally limited to visual presentation: `palette`, `font_family`, `font_size`, `line_width`, `marker_size`, `layout`, `legend_position`, `panel_spacing`, `background`, `axis_style`, `annotation_style`, and `export_preference`. Values are user-defined strings or numbers. Unknown attributes are ignored.

## Profile generation

```bash
python scripts/learn_style_profile.py feedback.jsonl --output style_profile.json
```

The profile records counts and selected preferences by figure type. A preference is applied only when its accepted/rejected evidence reaches the configured minimum support and accepted feedback exceeds rejected feedback. Neutral feedback is excluded from preference selection.

## Privacy and research integrity

- Obtain explicit permission before using project materials to infer reusable preferences.
- Keep feedback logs and profiles in the user-selected project directory; do not upload or transmit them by default.
- Store visual settings and feedback decisions only. Do not copy manuscript text, raw images, patient identifiers, unpublished data, credentials, or other sensitive content into the feedback log.
- For medical or otherwise sensitive projects, use de-identified visual metadata only and follow the user's data-handling requirements.
- Never use a user's research data to train a shared model or for unrelated projects.
- Do not treat a figure's visual appearance as a substitute for source data. Do not estimate missing measurements from pixels.
- If the user has not approved profile creation, perform the current figure task without retaining preferences.
