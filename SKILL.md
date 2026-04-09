---
name: data-viz-journalism
description: "Use this skill when the user wants to create charts, graphs, or static visualizations from data for journalistic publication. Trigger on 'make a chart', 'visualize', 'plot', 'graph', 'bar chart', 'line chart', or any request for publication-ready figures. Covers Altair (preferred), matplotlib, and plotly. Do NOT use for geographic maps (use dutch-choropleth-maps)."
---

## Purpose

Create publication-ready data visualisations for journalism. Clean, accessible, story-driven charts — not exploratory plots. Every chart must state the finding, not just show the data.

## When to use

User asks for a chart, graph, or visualisation from a DataFrame. Any request for bar charts, line charts, scatter plots, heatmaps, histograms, or publication-ready figures.

## When NOT to use

- **Geographic maps / choropleths** → use `dutch-choropleth-maps`
- **Data not yet analysed** → use `data-analysis-journalism` to find the story first
- **Data not yet clean** → use `data-cleaning-dutch` first

## Language

Respond in Dutch if the user writes in Dutch. Use Dutch labels in all visualisations unless told otherwise.

---

## Library preference order

1. **Altair** (voorkeur) — declaratief, schone standaardstijl, uitstekend voor statistische visualisatie. Gebruik voor: staafdiagrammen, lijndiagrammen, spreidingsdiagrammen, small multiples, heatmaps.
2. **Plotly** — wanneer interactiviteit nodig is (HTML-embeds voor webart ikelen).
3. **Matplotlib** — wanneer nauwkeurige controle nodig is of Altair het grafiektype niet aankan.

---

## Chart selection guide

Use this decision tree:

| Doel | Grafiektype | Bibliotheek |
|------|-------------|-------------|
| Categorieën vergelijken | Staafdiagram (horizontaal bij >5 categorieën of lange labels) | Altair |
| Trend over tijd | Lijndiagram (max. 5–6 lijnen) | Altair |
| Aandeel van geheel | Gestapeld staafdiagram (NOOIT taartdiagram) | Altair |
| Verband tussen 2 variabelen | Spreidingsdiagram | Altair |
| 2 dimensies vergelijken | Heatmap of small multiples | Altair |
| Verdeling | Histogram of boxplot | Altair / Matplotlib |

**Over taartdiagrammen**: gebruik ze nooit. Ze zijn moeilijk af te lezen bij meer dan 2 segmenten. Gebruik altijd een gestapeld staafdiagram of een gerangschikte staafgrafiek als alternatief.

---

## Journalism-specific rules

1. **Titel formuleert de bevinding, niet de data**: "Amsterdam heeft de hoogste huurstijging" — niet "Huurprijzen per gemeente". De titel is de kop.
2. **Ondertitel geeft context**: Methode, tijdperiode, bron. Voorbeeld: "Gemiddelde huurstijging per jaar, 2020–2024. Bron: CBS StatLine"
3. **Aslabels in begrijpelijke taal**: "Percentage woningen met energielabel A" — niet "pct_label_a"
4. **Bronvermelding**: Altijd "Bron: CBS StatLine" (of andere bron) als annotatie onderaan.
5. **Kleurblindveilig**: Gebruik colorblind-safe paletten. Standaard: Tableau10 in Altair.
6. **Geen chartjunk**: Verwijder onnodige rasterlijnen en randen; gebruik directe labels in plaats van legenda waar mogelijk.
7. **Markeer het verhaal**: Gebruik kleurcontrast om de kernbevinding te benadrukken. Maak niet-focale datapunten grijs. Annoteer het sleuteldatapunt.

---

## Altair templates

### Installatie

```bash
uv pip install altair vl-convert-python  # vl-convert is nodig voor PNG/SVG export
# of: pip install altair vl-convert-python
```

### Horizontaal staafdiagram (journalism stijl)

```python
import altair as alt
import pandas as pd

# Activeer de journalism-thema (laad assets/journalism_style.py)
# from journalism_style import altair_journalism_theme
# alt.themes.register('journalism', altair_journalism_theme)
# alt.themes.enable('journalism')

grafiek = alt.Chart(df).mark_bar().encode(
    x=alt.X('waarde:Q', title='Percentage woningen met zonnepanelen'),
    y=alt.Y('gemeente:N', sort='-x', title=None),
    color=alt.condition(
        alt.datum.gemeente == 'Utrecht',  # Markeer het verhaalfocus
        alt.value('#d62728'),             # Rood voor focus
        alt.value('#bdbdbd')              # Grijs voor de rest
    ),
    tooltip=['gemeente:N', alt.Tooltip('waarde:Q', format='.1f')]
).properties(
    title={
        'text': 'Utrecht loopt voorop met zonnepanelen',
        'subtitle': 'Aandeel woningen met zonnepanelen, 2024. Bron: CBS StatLine'
    },
    width=500,
    height=400
)
grafiek
```

### Lijndiagram met annotatie

```python
lijn = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('jaar:O', title='Jaar'),
    y=alt.Y('waarde:Q', title='Aantal warmtepompen (×1000)'),
    color=alt.Color('regio:N', title='Regio'),
    tooltip=['jaar:O', 'regio:N', alt.Tooltip('waarde:Q', format='.1f')]
)

annotatie_data = pd.DataFrame({
    'jaar': ['2022'],
    'waarde': [45],
    'tekst': ['Subsidieregeling ISDE verruimd']
})
annotatie = alt.Chart(annotatie_data).mark_text(
    align='left', dx=5, fontSize=11, color='#333'
).encode(
    x='jaar:O',
    y='waarde:Q',
    text='tekst:N'
)

(lijn + annotatie).properties(
    title={
        'text': 'Warmtepompen in opkomst sinds 2020',
        'subtitle': 'Aantal geïnstalleerde warmtepompen per regio. Bron: CBS StatLine'
    },
    width=600,
    height=350
)
```

### Spreidingsdiagram met regressielijn

```python
punten = alt.Chart(df).mark_circle(opacity=0.6).encode(
    x=alt.X('inkomen_mediaan:Q', title='Mediaan inkomen (×1000 €)'),
    y=alt.Y('zonnepanelen_pct:Q', title='% woningen met zonnepanelen'),
    size=alt.Size('aantal_woningen:Q', title='Aantal woningen'),
    color=alt.Color('provincie:N', title='Provincie'),
    tooltip=['gemeente:N', 'inkomen_mediaan:Q', 'zonnepanelen_pct:Q']
)

regressie = punten.transform_regression(
    'inkomen_mediaan', 'zonnepanelen_pct'
).mark_line(color='grey', strokeDash=[4, 4])

(punten + regressie).properties(
    title={
        'text': 'Rijkere gemeenten hebben niet per se meer zonnepanelen',
        'subtitle': 'Elke cirkel = één gemeente. Grootte = aantal woningen. Bron: CBS StatLine'
    },
    width=600,
    height=400
)
```

### Small multiples (facet per provincie)

```python
alt.Chart(df).mark_bar().encode(
    x=alt.X('jaar:O', title=None),
    y=alt.Y('waarde:Q', title='Waarde'),
    color=alt.value('#1f77b4')
).properties(
    width=120,
    height=80
).facet(
    facet='provincie:N',
    columns=4
).properties(
    title='Ontwikkeling per provincie'
)
```

---

## Plotly templates (voor interactief)

```python
import plotly.express as px

# Interactief staafdiagram
fig = px.bar(
    df.sort_values('waarde', ascending=False),
    x='gemeente',
    y='waarde',
    title='Utrecht loopt voorop met zonnepanelen',
    labels={'waarde': '% woningen met zonnepanelen', 'gemeente': ''},
    color='waarde',
    color_continuous_scale='Blues'
)
fig.update_layout(
    title_subtitle_text='Aandeel woningen met zonnepanelen, 2024. Bron: CBS StatLine',
    showlegend=False,
    plot_bgcolor='white'
)
fig.write_html('output/grafiek.html')
```

---

## Saving figures

Always save both a high-resolution PNG and a vector format:

```python
import os
os.makedirs('output', exist_ok=True)

# Altair — vereist vl-convert-python
grafiek.save('output/grafiek.png', scale_factor=2)   # 2× voor retina/druk
grafiek.save('output/grafiek.svg')                    # Vector voor publicatie

# Plotly
fig.write_image('output/grafiek.png', scale=2, width=800, height=500)
fig.write_html('output/grafiek.html')                 # Interactief embed

# Matplotlib
plt.savefig('output/grafiek.png', dpi=300, bbox_inches='tight')
plt.savefig('output/grafiek.svg', bbox_inches='tight')
```

---

## Output format

Every visualisation must include:

1. **De grafiek zelf** — opgeslagen als PNG + SVG (of HTML voor interactief)
2. **Alt-tekst** — één zin die beschrijft wat de grafiek toont (voor toegankelijkheid)
3. **Bronvermelding** — "Bron: CBS StatLine" (of andere bron)

Voorbeeld alt-tekst: "Horizontaal staafdiagram van 10 Nederlandse gemeenten, gerangschikt op percentage woningen met zonnepanelen. Utrecht staat bovenaan met 34%, het landelijk gemiddelde is 18%."

---

## Journalism style module

For a reusable style module with the journalism colour palette and Altair theme registration:

→ Load `assets/journalism_style.py` and follow the usage instructions at the top of the file.

## Extended reference

For chart type decision tree, code templates for every chart type in Altair/matplotlib/plotly, colour palette definitions, typography and sizing for web vs. print, small multiples patterns, and annotation recipes:

→ Read `references/chart-selection-guide.md`
