# data-viz-journalism

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI agent skill for creating publication-ready data visualizations for journalism. Generates charts using Altair (preferred), Plotly (interactive), or matplotlib (fine-grained control). Journalism rules built in: title states the finding (not the variable), subtitle includes source and period, colorblind-safe Tableau10 palette, no pie charts (stacked bars instead), direct labels over legends. Includes `assets/journalism_style.py` — a reusable Python module with a color palette, Altair theme, matplotlib style helpers, and choropleth colormap definitions. Exports to PNG + SVG for print/web. Responds in Dutch if user writes in Dutch.

Compatible with Claude Code, Open Code, Kilo Code, Cursor, Windsurf, Cline, Aider, and 40+ other AI coding tools.

## Overview

This skill transforms an AI agent into a knowledgeable data visualization partner for journalism that can:

- Select the right chart type for the story (no pie charts — stacked bars instead)
- Apply journalism-specific title and subtitle conventions
- Highlight the key finding using color contrast
- Use colorblind-safe palettes (Tableau10 by default)
- Export publication-ready PNG (retina) and SVG files
- Apply the reusable `journalism_style.py` module for consistent styling

## Installation

### Dependencies

```bash
pip install altair matplotlib plotly vl-convert-python
```

`vl-convert-python` is required for PNG and SVG export from Altair.

### Quick Install (Any Agent)

If you use the [Vercel Skills CLI](https://github.com/vercel-labs/skills), this works across 40+ agents:

```bash
npx skills add linksmith/data-viz-journalism
```

See below for tool-specific instructions.

### Cursor

**Option 1: Clone to Cursor rules directory**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git ~/.cursor/rules/data-viz-journalism
```

**Option 2: Add to project `.cursorrules`**

```bash
# In your project root
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o .cursorrules
```

**Option 3: Project-level installation**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git .cursor/data-viz-journalism
```

Then reference in `.cursorrules`:
```
Use the data-viz-journalism skill in .cursor/data-viz-journalism/ for all journalism visualization tasks.
```

### Windsurf (Codeium)

**Option 1: Global rules**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git ~/.windsurf/rules/data-viz-journalism
```

**Option 2: Project-level**

Create `.windsurf/rules/data-viz-journalism.md` in your project:
```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o .windsurf/rules/data-viz-journalism.md
```

### Claude Code / Open Code / Kilo Code

All three tools support the same plugin format:

**Option 1: Install as a plugin** (recommended, no npm/node required)

```bash
claude plugin install --from https://github.com/linksmith/data-viz-journalism
```

Replace `claude` with `open` or `kilo` depending on your tool.

**Option 2: Add as a project skill**

```bash
mkdir -p .claude/skills
git clone https://github.com/linksmith/data-viz-journalism.git .claude/skills/data-viz-journalism
```

**Option 3: Add as a slash command**

```bash
mkdir -p .claude/commands
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md \
  -o .claude/commands/data-viz-journalism.md
```

### Cline (VS Code Extension)

**Option 1: Add to .clinerules**

```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o .clinerules
```

**Option 2: Workspace settings**

1. Clone the skill to your workspace:
```bash
git clone https://github.com/linksmith/data-viz-journalism.git .cline/data-viz-journalism
```

2. In VS Code settings, add to `cline.customInstructions`:
```
Use data-viz-journalism skill for publication-ready charts. See .cline/data-viz-journalism/SKILL.md
```

### Roo Code (VS Code Extension)

**Option 1: Add to .roorules**

```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o .roorules
```

**Option 2: Custom instructions**

In VS Code, open Roo Code settings and add to Custom Instructions:
```
For journalism visualization, reference the skill at:
https://github.com/linksmith/data-viz-journalism

Download assets/journalism_style.py for reusable styling.
```

### Aider

**Option 1: Add as read-only context**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git ~/skills/data-viz-journalism

aider --read ~/skills/data-viz-journalism/SKILL.md \
      --read ~/skills/data-viz-journalism/assets/journalism_style.py
```

**Option 2: Add to .aider.conf.yml**

```yaml
read:
  - ~/skills/data-viz-journalism/SKILL.md
  - ~/skills/data-viz-journalism/assets/journalism_style.py
  - ~/skills/data-viz-journalism/references/chart-selection-guide.md
```

### OpenHands

**Option 1: Add to workspace**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git .openhands/data-viz-journalism
```

**Option 2: Custom instructions**

Add to `.openhands/instructions.md`:
```
For journalism data visualization:
1. Read .openhands/data-viz-journalism/SKILL.md for chart rules
2. Use assets/journalism_style.py for consistent styling
3. Reference references/chart-selection-guide.md for chart type selection
```

### Goose (Block)

**Option 1: Add to Goose extensions**

```bash
git clone https://github.com/linksmith/data-viz-journalism.git ~/.goose/extensions/data-viz-journalism
```

**Option 2: Add instruction file**

```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o ~/.goose/instructions/data-viz-journalism.md
```

### GitHub Copilot

**Option 1: Add to .github/copilot-instructions.md**

```bash
mkdir -p .github
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o .github/copilot-instructions.md
```

**Option 2: Reference in VS Code settings**

In `.vscode/settings.json`:
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": ".github/copilot-instructions.md"
    }
  ]
}
```

### Generic AI Assistants

For any AI assistant that supports custom instructions or context files:

1. Download the SKILL.md file:
```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/SKILL.md -o data-viz-journalism-instructions.md
```

2. Paste the contents into your AI assistant's custom instructions or system prompt.

3. For reusable styling, also download `assets/journalism_style.py`:
```bash
curl -L https://raw.githubusercontent.com/linksmith/data-viz-journalism/main/assets/journalism_style.py -o journalism_style.py
```

## Usage

### journalism_style.py

The included Python module provides a consistent color palette and Altair theme for all journalism charts.

```python
from assets.journalism_style import COLORS, altair_journalism_theme
import altair as alt

alt.themes.register('journalism', altair_journalism_theme)
alt.themes.enable('journalism')
```

### Example Workflow

```python
import altair as alt
import pandas as pd
from assets.journalism_style import COLORS, altair_journalism_theme

# Register and enable the journalism theme
alt.themes.register('journalism', altair_journalism_theme)
alt.themes.enable('journalism')

# Create a journalism-style bar chart
grafiek = alt.Chart(df).mark_bar().encode(
    x=alt.X('waarde:Q', title='Percentage woningen met zonnepanelen'),
    y=alt.Y('gemeente:N', sort='-x', title=None),
    color=alt.condition(
        alt.datum.gemeente == 'Utrecht',
        alt.value(COLORS['focus']),   # Red for the story focus
        alt.value(COLORS['muted'])    # Grey for context
    )
).properties(
    title={
        'text': 'Utrecht loopt voorop met zonnepanelen',
        'subtitle': 'Aandeel woningen met zonnepanelen, 2024. Bron: CBS StatLine'
    },
    width=500,
    height=400
)

# Save for print and web
import os
os.makedirs('output', exist_ok=True)
grafiek.save('output/grafiek.png', scale_factor=2)  # Retina/print
grafiek.save('output/grafiek.svg')                   # Vector
```

### Example Prompts

- "Maak een staafdiagram van de top 10 gemeenten"
- "Markeer de uitschieter in mijn grafiek"
- "Sla de grafiek op als PNG en SVG"
- "Gebruik een kleurenschema dat kleurenblindveilig is"

## Skill Structure

```
data-viz-journalism/
├── SKILL.md                           # Skill definition (chart selection, journalism rules, templates)
├── assets/
│   └── journalism_style.py            # Reusable Python style module (COLORS, Altair theme, matplotlib helpers)
├── references/
│   └── chart-selection-guide.md       # Chart type decision tree and code templates
└── evals.json                         # Evaluation prompts for skill testing
```

## Features

### journalism_style.py Module

The included Python module provides:

- **COLORS dict** — Named color constants: `focus` (red), `primary` (blue), `muted` (grey), `positive` (green), `palette` (full Tableau10)
- **Altair theme** — `altair_journalism_theme()` registers clean typography, no grid lines, and Tableau10 color scheme
- **Matplotlib helpers** — Style helpers for setting journalism-compliant figure styling
- **Choropleth colormaps** — Named colormap definitions for geographic visualizations

### Journalism Rules Built In

1. **Title states the finding** — "Amsterdam heeft de hoogste huurstijging" not "Huurprijzen per gemeente"
2. **Subtitle includes context** — Method, time period, source: "Gemiddelde huurstijging per jaar, 2020–2024. Bron: CBS StatLine"
3. **No pie charts** — Always replaced by stacked bars or ranked bar charts
4. **Colorblind-safe palette** — Tableau10 by default; never red-green as the primary distinction
5. **Story highlighting** — Focus color for key data point, muted grey for context
6. **Direct labels** — Preferred over legends where possible
7. **Source attribution** — "Bron: [source]" annotation on every chart

### Export Formats

- **PNG at 2x resolution** — For retina displays and print (via `vl-convert-python`)
- **SVG** — Vector format for publication and scaling
- **HTML** — For interactive Plotly embeds in web articles

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

- **Issue Tracker:** https://github.com/linksmith/data-viz-journalism/issues
- **Pull Requests:** https://github.com/linksmith/data-viz-journalism/pulls

## Resources

- [Altair Documentation](https://altair-viz.github.io/)
- [vl-convert-python](https://github.com/vega/vl-convert) — Required for PNG/SVG export from Altair
- [Tableau10 Colorblind Guide](https://www.tableau.com/about/blog/2016/7/colors-upgrade-tableau-10-56782)
- [CBS StatLine Open Data](https://opendata.cbs.nl/)
