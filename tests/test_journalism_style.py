"""
Unit tests for journalism_style.py — the immutable style contract of the
data-viz-journalism skill.

journalism_style.py defines the visual grammar used across all workshop
visualisations (Altair charts, Matplotlib figures, and choropleth maps).
These tests enforce that contract: a change to any value tested here is a
deliberate decision that must also update teaching materials, slide decks,
and student exercise templates.  If a test breaks after an edit to
journalism_style.py, stop and ask whether the change was intentional.

Run with:
    pytest .kilo/skills/data-viz-journalism/tests/test_journalism_style.py -v
"""

import re

import pytest
import matplotlib.pyplot as plt

from journalism_style import (
    COLORS,
    MAP_COLORMAPS,
    altair_journalism_theme,
    apply_matplotlib_journalism_style,
)


# ---------------------------------------------------------------------------
# COLORS dict
# ---------------------------------------------------------------------------

def test_colors_has_required_keys():
    """COLORS must expose every semantic role used in workshop chart templates."""
    required = {"focus", "primary", "muted", "positive", "negative", "palette"}
    missing = required - set(COLORS.keys())
    assert not missing, f"COLORS is missing required keys: {missing}"


def test_colors_palette_length_and_format():
    """Palette must contain exactly 10 valid CSS hex colours."""
    palette = COLORS["palette"]
    assert len(palette) == 10, (
        f"Expected 10 palette colours, found {len(palette)}"
    )
    hex_pattern = re.compile(r"^#[0-9a-fA-F]{6}$")
    bad = [c for c in palette if not hex_pattern.match(c)]
    assert not bad, f"Palette entries are not valid 6-digit hex colours: {bad}"


def test_focus_equals_negative():
    """COLORS['focus'] and COLORS['negative'] must be the same colour.

    This is a documented design decision: both roles use the same alert red
    so that a 'focus highlight' and a 'negative value' are visually identical.
    If these drift apart, workshop exercises that rely on the equivalence will
    produce inconsistent charts.
    """
    assert COLORS["focus"] == COLORS["negative"], (
        f"focus ({COLORS['focus']}) != negative ({COLORS['negative']}). "
        "These must remain identical — see style contract."
    )


# ---------------------------------------------------------------------------
# altair_journalism_theme()
# ---------------------------------------------------------------------------

def test_altair_theme_structure():
    """Theme dict has the top-level 'config' key with all required sub-keys."""
    theme = altair_journalism_theme()
    assert isinstance(theme, dict), "altair_journalism_theme() must return a dict"
    assert "config" in theme, "Theme missing top-level 'config' key"
    config = theme["config"]
    for key in ("background", "axis", "title", "legend", "bar", "line"):
        assert key in config, f"Theme config missing required key '{key}'"


def test_altair_theme_background_white():
    """Chart background must be plain white — no off-white or transparent."""
    assert altair_journalism_theme()["config"]["background"] == "white"


def test_altair_theme_no_frame():
    """View strokeWidth must be 0 to suppress the default chart border."""
    stroke = altair_journalism_theme()["config"]["view"]["strokeWidth"]
    assert stroke == 0, f"Expected strokeWidth=0, got {stroke}"


def test_altair_theme_title_size_and_weight():
    """Title typography: 16 px, bold — matches the journalism house style."""
    title = altair_journalism_theme()["config"]["title"]
    assert title["fontSize"] == 16, (
        f"Title fontSize should be 16, got {title['fontSize']}"
    )
    assert title["fontWeight"] == "bold", (
        f"Title fontWeight should be 'bold', got {title['fontWeight']}"
    )


def test_altair_theme_axis_label_size():
    """Axis labels must be 12 px for legibility in small multiples."""
    label_size = altair_journalism_theme()["config"]["axis"]["labelFontSize"]
    assert label_size == 12, (
        f"Axis labelFontSize should be 12, got {label_size}"
    )


def test_altair_theme_grid_subtle():
    """Grid opacity must be strictly below 1.0 so data ink dominates the grid."""
    grid_opacity = altair_journalism_theme()["config"]["axis"]["gridOpacity"]
    assert grid_opacity < 1.0, (
        f"gridOpacity should be < 1.0 for a subtle grid, got {grid_opacity}"
    )


def test_altair_theme_registers_without_error():
    """Theme can be registered and enabled in Altair without raising exceptions."""
    alt = pytest.importorskip("altair", reason="altair not installed")
    alt.themes.register("journalism", altair_journalism_theme)
    alt.themes.enable("journalism")      # must not raise
    alt.themes.enable("default")         # restore default so other tests are unaffected


# ---------------------------------------------------------------------------
# apply_matplotlib_journalism_style()
# ---------------------------------------------------------------------------

def test_matplotlib_style_removes_spines():
    """Top and right spines must be hidden to match the minimal journalism look."""
    fig, ax = plt.subplots()
    try:
        apply_matplotlib_journalism_style(ax)
        assert ax.spines["top"].get_visible() is False, "Top spine should be hidden"
        assert ax.spines["right"].get_visible() is False, "Right spine should be hidden"
    finally:
        plt.close(fig)


def test_matplotlib_style_source_annotation():
    """Source text must appear in fig.texts when fig is supplied."""
    fig, ax = plt.subplots()
    try:
        apply_matplotlib_journalism_style(ax, fig=fig, source_text="Bron: Test")
        texts = [t.get_text() for t in fig.texts]
        assert any("Bron: Test" in t for t in texts), (
            f"'Bron: Test' not found in fig.texts: {texts}"
        )
    finally:
        plt.close(fig)


def test_matplotlib_style_no_fig_no_crash():
    """Calling with no fig argument (default) must not raise any exception."""
    fig, ax = plt.subplots()
    try:
        apply_matplotlib_journalism_style(ax)   # fig omitted intentionally
    finally:
        plt.close(fig)


# ---------------------------------------------------------------------------
# MAP_COLORMAPS
# ---------------------------------------------------------------------------

def test_map_colormaps_keys():
    """MAP_COLORMAPS must expose all four colourmap roles used in workshop maps."""
    required = {"sequential", "sequential_blue", "diverging", "qualitative"}
    missing = required - set(MAP_COLORMAPS.keys())
    assert not missing, f"MAP_COLORMAPS is missing required keys: {missing}"


def test_map_colormaps_sequential_is_ylorrd():
    """Default sequential colourmap must be 'YlOrRd'.

    This is a documented design decision: YlOrRd is the standard for Dutch
    data journalism choropleth maps (high contrast, print-safe, accessible).
    Changing it would silently break the map colour guidance in the workshop.
    """
    assert MAP_COLORMAPS["sequential"] == "YlOrRd", (
        f"Expected 'YlOrRd', got '{MAP_COLORMAPS['sequential']}'. "
        "This is a documented design decision — see style contract."
    )
