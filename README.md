# essay-picture-beautify

A research-figure enhancement skill. Start with `SKILL.md`.

Includes 14 figure-type guidelines, visual design guidance, research-paper cases, an index of provided documents, and three command-line utilities.

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
```

Dependencies: Python 3, PyMuPDF (`fitz`), pandas, matplotlib, Pillow. Figure outputs should always be checked against original paper text and scientific data.
