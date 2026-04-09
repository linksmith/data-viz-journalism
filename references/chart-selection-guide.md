# Chart Selection Guide — Datajournalistiek

Uitgebreide gids voor grafiektype-selectie, code-templates en stijlconventies voor publicatierijpe visualisaties.

---

## 1. Beslisboom voor grafiekkeuze

```
Wat wil je laten zien?
│
├── Categorieën vergelijken
│   ├── ≤5 categorieën, korte labels → Verticaal staafdiagram
│   └── >5 categorieën of lange labels → Horizontaal staafdiagram (gesorteerd)
│
├── Ontwikkeling over tijd
│   ├── 1–5 groepen → Lijndiagram
│   ├── >5 groepen → Small multiples (facets)
│   └── Slechts 2 tijdpunten → Dumbbell chart (paar)
│
├── Aandeel van geheel
│   ├── Vergelijk aandelen meerdere categorieën → Gestapeld staafdiagram (100%)
│   └── NOOIT → Taartdiagram
│
├── Verband tussen 2 variabelen
│   ├── Beide continu → Spreidingsdiagram (+ regressielijn)
│   └── Een categorisch, een continu → Box plot of violin plot
│
├── Twee dimensies vergelijken (matrix)
│   ├── Weinig rijen/kolommen → Heatmap
│   └── Veel categorieën → Small multiples
│
└── Verdeling van één variabele
    ├── Één groep → Histogram
    └── Meerdere groepen vergelijken → Box plot of violin plot
```

---

## 2. Altair — code-templates per grafiektype

### Verticaal staafdiagram

```python
import altair as alt

alt.Chart(df).mark_bar().encode(
    x=alt.X('categorie:N', sort='-y', title=None),
    y=alt.Y('waarde:Q', title='Waarde-eenheid'),
    color=alt.value('#1f77b4'),
    tooltip=['categorie:N', alt.Tooltip('waarde:Q', format='.1f')]
).properties(
    title={'text': 'Bevinding als kop', 'subtitle': 'Context. Bron: CBS StatLine'},
    width=500,
    height=300
)
```

### Horizontaal staafdiagram (aanbevolen bij >5 categorieën)

```python
alt.Chart(df).mark_bar().encode(
    y=alt.Y('categorie:N', sort='-x', title=None),
    x=alt.X('waarde:Q', title='Waarde-eenheid'),
    color=alt.condition(
        alt.datum.categorie == 'Focus gemeente',
        alt.value('#d62728'),   # Rood voor focus
        alt.value('#bdbdbd')    # Grijs voor de rest
    ),
    tooltip=['categorie:N', alt.Tooltip('waarde:Q', format='.1f')]
).properties(
    title={'text': 'Bevinding als kop', 'subtitle': 'Context. Bron: CBS StatLine'},
    width=500,
    height=400
)
```

### Lijndiagram

```python
alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('jaar:O', title='Jaar'),
    y=alt.Y('waarde:Q', title='Waarde-eenheid'),
    color=alt.Color('groep:N', title='Groep'),
    strokeDash=alt.StrokeDash('groep:N'),  # Patroon voor kleurblindveiligheid
    tooltip=['jaar:O', 'groep:N', alt.Tooltip('waarde:Q', format='.1f')]
).properties(
    title={'text': 'Bevinding als kop', 'subtitle': 'Context. Bron: CBS StatLine'},
    width=600,
    height=350
)
```

### Gestapeld staafdiagram — 100% (aandelen)

```python
alt.Chart(df).mark_bar().encode(
    x=alt.X('jaar:O', title='Jaar'),
    y=alt.Y('aandeel:Q', stack='normalize', axis=alt.Axis(format='%'), title='Aandeel'),
    color=alt.Color('categorie:N', title='Categorie'),
    tooltip=['jaar:O', 'categorie:N', alt.Tooltip('aandeel:Q', format='.1%')]
).properties(
    title={'text': 'Bevinding als kop', 'subtitle': 'Aandelen per jaar. Bron: CBS StatLine'},
    width=500,
    height=300
)
```

### Heatmap

```python
alt.Chart(df).mark_rect().encode(
    x=alt.X('jaar:O', title='Jaar'),
    y=alt.Y('gemeente:N', title=None),
    color=alt.Color('waarde:Q',
                    scale=alt.Scale(scheme='yelloworangered'),
                    title='Waarde'),
    tooltip=['gemeente:N', 'jaar:O', alt.Tooltip('waarde:Q', format='.1f')]
).properties(
    title={'text': 'Bevinding als kop', 'subtitle': 'Context. Bron: CBS StatLine'},
    width=400,
    height=500
)
```

### Small multiples (facets per provincie)

```python
alt.Chart(df).mark_line().encode(
    x=alt.X('jaar:O', title=None),
    y=alt.Y('waarde:Q', title='Waarde'),
    color=alt.value('#1f77b4')
).properties(
    width=150,
    height=100
).facet(
    facet='provincie:N',
    columns=4
).properties(
    title='Bevinding als kop'
)
```

### Dumbbell chart (voor twee tijdpunten)

```python
import pandas as pd

# Voorbereiding: twee rijen per gemeente (voor en na)
basis = alt.Chart(df).encode(
    y=alt.Y('gemeente:N', sort='-x', title=None)
)

punten = basis.mark_circle(size=80).encode(
    x=alt.X('waarde:Q', title='Waarde'),
    color=alt.Color('jaar:N', title='Jaar')
)

lijn = basis.mark_rule(strokeWidth=2, color='#aaa').encode(
    x='min(waarde):Q',
    x2='max(waarde):Q'
)

(lijn + punten).properties(
    title={'text': 'Verandering tussen twee jaren', 'subtitle': 'Bron: CBS StatLine'},
    width=450,
    height=400
)
```

---

## 3. Matplotlib — templates

### Staafdiagram met bronvermelding

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig, ax = plt.subplots(figsize=(10, 6))

kleuren = ['#d62728' if g == 'Focus' else '#bdbdbd' for g in df['gemeente']]
bars = ax.barh(df['gemeente'], df['waarde'], color=kleuren)

ax.set_xlabel('Waarde-eenheid', fontsize=12)
ax.set_title('Bevinding als kop', fontsize=16, fontweight='bold', pad=15)
ax.invert_yaxis()  # Hoogste bovenaan

# Directe labels op staven
for bar in bars:
    breedte = bar.get_width()
    ax.text(breedte + 0.3, bar.get_y() + bar.get_height()/2,
            f'{breedte:.1f}', va='center', fontsize=10)

# Bronvermelding
fig.text(0.02, 0.01, 'Bron: CBS StatLine', fontsize=8, color='grey',
         transform=fig.transFigure)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('output/grafiek.png', dpi=300, bbox_inches='tight')
plt.savefig('output/grafiek.svg', bbox_inches='tight')
```

### Lijndiagram met referentielijn

```python
fig, ax = plt.subplots(figsize=(12, 6))

for groep in df['groep'].unique():
    data = df[df['groep'] == groep]
    ax.plot(data['jaar'], data['waarde'], marker='o', label=groep, linewidth=2)

# Referentielijn (bijv. landelijk gemiddelde)
ax.axhline(y=landelijk_gemiddelde, color='grey', linestyle='--',
           linewidth=1, label='Landelijk gemiddelde')

ax.set_title('Bevinding als kop', fontsize=16, fontweight='bold')
ax.set_xlabel('Jaar')
ax.set_ylabel('Waarde-eenheid')
ax.legend(loc='upper left', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.text(0.02, 0.01, 'Bron: CBS StatLine', fontsize=8, color='grey')
plt.tight_layout(rect=[0, 0.03, 1, 1])
```

---

## 4. Plotly — templates

### Interactief horizontaal staafdiagram

```python
import plotly.express as px
import plotly.graph_objects as go

fig = px.bar(
    df.sort_values('waarde', ascending=True),
    x='waarde',
    y='gemeente',
    orientation='h',
    title='Bevinding als kop',
    labels={'waarde': 'Waarde-eenheid', 'gemeente': ''},
    color='waarde',
    color_continuous_scale='Blues'
)
fig.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    font_size=12,
    annotations=[{
        'text': 'Bron: CBS StatLine',
        'x': 0, 'y': -0.12,
        'xref': 'paper', 'yref': 'paper',
        'showarrow': False, 'font': {'size': 10, 'color': 'grey'}
    }]
)
fig.write_html('output/grafiek.html')
```

### Interactief lijndiagram

```python
fig = px.line(
    df,
    x='jaar',
    y='waarde',
    color='groep',
    title='Bevinding als kop',
    labels={'waarde': 'Waarde-eenheid', 'jaar': 'Jaar', 'groep': 'Groep'},
    markers=True
)
fig.update_layout(
    plot_bgcolor='white',
    hovermode='x unified'
)
fig.write_html('output/grafiek.html')
```

---

## 5. Kleurpaletten

### Kleurblindveilig — journalistiek palet (op basis van Tableau10)

```python
KLEUREN = {
    'focus': '#d62728',        # Rood — voor het focusdatapunt
    'primair': '#1f77b4',      # Blauw — voor de hoofdserie
    'gedimpt': '#bdbdbd',      # Grijs — voor niet-focusdata
    'positief': '#2ca02c',     # Groen — voor groei/vooruitgang
    'negatief': '#d62728',     # Rood — voor daling/achterstand
    'palet': [
        '#1f77b4',  # Blauw
        '#ff7f0e',  # Oranje
        '#2ca02c',  # Groen
        '#d62728',  # Rood
        '#9467bd',  # Paars
        '#8c564b',  # Bruin
        '#e377c2',  # Roze
        '#7f7f7f',  # Grijs
        '#bcbd22',  # Geel-groen
        '#17becf',  # Cyaan
    ]
}
```

### Kleurschalen voor kaarten

```python
# Sequentieel (voor hoeveelheden, van laag naar hoog)
SCHALEN_SEQUENTIEEL = ['YlOrRd', 'YlGnBu', 'Blues', 'Greens', 'Oranges']

# Divergerend (voor afwijking van gemiddelde, negatief ↔ positief)
SCHALEN_DIVERGEREND = ['RdBu_r', 'RdYlGn', 'PiYG']

# Kwalitatief (voor categorieën zonder ordening)
SCHALEN_KWALITATIEF = ['Set2', 'Tableau10', 'Pastel1']
```

---

## 6. Typografie en formaten voor web vs. print

| Eigenschap | Web (HTML/SVG) | Print (PNG 300 dpi) |
|-----------|----------------|---------------------|
| Titelfontgrootte | 16–18px | 18–22pt |
| Aslabelfontgrootte | 12–13px | 12–14pt |
| Annotatiefontgrootte | 10–11px | 10–12pt |
| Breedte grafiek | 600–800px | 15–20 cm |
| Hoogte grafiek | Afhankelijk van inhoud | Afhankelijk van inhoud |
| Kleurresolutie | 72–96 dpi | 300 dpi minimum |
| Exportformaat | SVG + HTML | PNG (300dpi) + SVG |

### Aanbevolen afmetingen Altair

```python
# Webpublicatie
grafiek.properties(width=600, height=400)

# Mobiel-vriendelijk (smaller)
grafiek.properties(width=380, height=280)

# Print (in pixels bij 300dpi → omrekenen naar cm: pixels / 118)
grafiek.properties(width=709, height=591)  # ≈ 6×5 inch bij 300dpi
```

---

## 7. Annotatiepatronen

### Referentielijn met label (Altair)

```python
import pandas as pd

referentie_data = pd.DataFrame({'waarde': [landelijk_gemiddelde], 'label': ['Landelijk gemiddelde']})

lijn = alt.Chart(referentie_data).mark_rule(
    strokeDash=[4, 4], color='grey', strokeWidth=1
).encode(x='waarde:Q')

label = alt.Chart(referentie_data).mark_text(
    align='left', dx=4, dy=-6, fontSize=10, color='grey'
).encode(x='waarde:Q', text='label:N')

(hoofdgrafiek + lijn + label)
```

### Callout op specifiek datapunt (Altair)

```python
callout_data = df[df['gemeente'] == 'Utrecht'].copy()
callout_data['tekst'] = 'Utrecht: 34,2%'

callout = alt.Chart(callout_data).mark_text(
    align='left', dx=8, fontSize=11, fontWeight='bold', color='#d62728'
).encode(
    x='waarde:Q',
    y='gemeente:N',
    text='tekst:N'
)

(hoofdgrafiek + callout)
```

### Tijdlijn-annotatie (periode markeren)

```python
periode_data = pd.DataFrame({'start': [2020], 'einde': [2022], 'label': ['Coronaperiode']})

periodemarkering = alt.Chart(periode_data).mark_rect(
    opacity=0.1, color='grey'
).encode(
    x='start:O',
    x2='einde:O'
)

periode_label = alt.Chart(periode_data).mark_text(
    align='center', dy=-10, fontSize=10, color='grey'
).encode(
    x=alt.X('start:O'),
    text='label:N'
)

(lijndiagram + periodemarkering + periode_label)
```
