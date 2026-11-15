# essay-picture-beautify

A research-figure enhancement skill. Start with `SKILL.md`.

Includes 14 figure-type guidelines, visual design guidance, research-paper cases, an index of provided documents, and four command-line utilities. The personalized optimization feature learns presentation preferences from explicit user feedback and selected project references.

## Setup

Install the Python dependencies before running the command-line utilities:

```bash
python -m pip install -r requirements.txt
```

The skill entry point is `SKILL.md`; keep `references/`, `scripts/` and `examples/` alongside it when installing the skill in your agent's skill directory.

The files in `examples/` demonstrate the utilities and should not be cited as experimental evidence. Referenced source papers are not included; consult the original publications to verify the case-study notes.

## Examples

```bash
python scripts/inspect_paper.py paper.pdf --output figures.csv
python scripts/plot_results.py examples/sample_series.csv output/figure --x-label 'Epoch' --y-label 'Accuracy'
python scripts/compose_panels.py examples/panels.json output/panels.svg
python scripts/learn_style_profile.py examples/feedback_template.jsonl --output output/style_profile.json
```

Dependencies: Python 3, PyMuPDF (`fitz`), pandas, matplotlib, Pillow. Figure outputs should always be checked against original paper text and scientific data.

## Personalized optimization

With the user's explicit permission, use selected papers, original figures, numeric data, plotting sources and approved examples to infer project-specific visual settings. Then collect explicit accept/reject feedback and aggregate it into a local style profile by figure type. See `references/personalized_optimization.md`. This is local preference learning, not model-weight training. Project files and feedback are not transmitted by default.
