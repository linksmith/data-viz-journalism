"""
Journalism visualization style for Dutch data journalism.

Usage with Altair:
    import altair as alt
    from journalism_style import altair_journalism_theme, COLORS

    alt.themes.register('journalism', altair_journalism_theme)
    alt.themes.enable('journalism')

Usage as standalone colour reference:
    from journalism_style import COLORS
    highlight_color = COLORS['focus']
"""

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

COLORS = {
    'focus':    '#d62728',   # Red   — highlight the story's key data point
    'primary':  '#1f77b4',   # Blue  — main data series
    'muted':    '#bdbdbd',   # Grey  — background / non-focal data
    'positive': '#2ca02c',   # Green — growth / progress
    'negative': '#d62728',   # Red   — decline / shortfall (same as focus)
    'palette': [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Grey
        '#bcbd22',  # Yellow-green
        '#17becf',  # Cyan
    ]
}

# ---------------------------------------------------------------------------
# Altair theme
# ---------------------------------------------------------------------------

def altair_journalism_theme():
    """
    Return an Altair theme dict with journalism-friendly defaults.

    Applies:
    - Clean white background, no frame stroke
    - Readable axis labels (12px) with medium-weight titles (13px)
    - Subtle grid (30% opacity)
    - Bold 16px chart title, smaller muted subtitle
    - Compact legend labels
    """
    return {
        'config': {
            'background': 'white',
            'view': {
                'strokeWidth': 0,
                'continuousWidth': 500,
                'continuousHeight': 350,
            },
            'axis': {
                'labelFontSize': 12,
                'labelColor': '#333333',
                'titleFontSize': 13,
                'titleColor': '#333333',
                'titleFontWeight': 'normal',
                'gridColor': '#e0e0e0',
                'gridOpacity': 0.5,
                'domainColor': '#cccccc',
                'tickColor': '#cccccc',
            },
            'axisX': {
                'labelAngle': 0,
            },
            'title': {
                'fontSize': 16,
                'fontWeight': 'bold',
                'color': '#111111',
                'subtitleFontSize': 12,
                'subtitleColor': '#666666',
                'subtitleFontWeight': 'normal',
                'anchor': 'start',
                'offset': 12,
            },
            'legend': {
                'labelFontSize': 11,
                'titleFontSize': 12,
                'titleFontWeight': 'normal',
            },
            'bar': {
                'fill': COLORS['primary'],
            },
            'line': {
                'strokeWidth': 2.5,
            },
            'point': {
                'size': 50,
            },
            'mark': {
                'tooltip': True,
            },
        }
    }


# ---------------------------------------------------------------------------
# Matplotlib style helpers
# ---------------------------------------------------------------------------

def apply_matplotlib_journalism_style(ax, fig=None, source_text='Bron: CBS StatLine'):
    """
    Apply journalism styling to a matplotlib Axes object in-place.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    fig : matplotlib.figure.Figure, optional
        If provided, adds a source annotation at the bottom-left.
    source_text : str
        Source attribution string.
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(colors='#555555', labelsize=11)
    ax.xaxis.label.set_color('#333333')
    ax.yaxis.label.set_color('#333333')
    ax.title.set_color('#111111')
    ax.title.set_fontsize(16)
    ax.title.set_fontweight('bold')
    ax.grid(axis='y', color='#e0e0e0', linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)

    if fig is not None:
        fig.text(
            0.02, 0.01,
            source_text,
            fontsize=9,
            color='#888888',
            transform=fig.transFigure
        )


# ---------------------------------------------------------------------------
# Sequential colour scales for choropleth maps
# ---------------------------------------------------------------------------

MAP_COLORMAPS = {
    'sequential': 'YlOrRd',    # Yellow → Orange → Red  (quantities)
    'sequential_blue': 'YlGnBu',
    'diverging': 'RdBu_r',     # Red ↔ Blue  (deviation from average)
    'qualitative': 'Set2',
}
