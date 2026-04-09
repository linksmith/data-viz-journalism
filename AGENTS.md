# data-viz-journalism Skill

AI agent skill for creating publication-ready data visualizations for journalism.

## Project structure

- `SKILL.md` — Skill definition (chart selection guide, journalism rules, templates)
- `assets/journalism_style.py` — Reusable Python style module (COLORS, Altair theme, matplotlib helpers)
- `references/chart-selection-guide.md` — Chart type decision tree and code templates
- `evals.json` — Evaluation prompts for skill testing

## Testing

```bash
pip install altair matplotlib plotly
python -c "from assets.journalism_style import COLORS, altair_journalism_theme; print('OK')"
```

Run the evals in `evals.json` manually. Pass threshold: all scoring_criteria met per eval.
