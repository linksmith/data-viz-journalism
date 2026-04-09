"""
Ensure journalism_style.py (in assets/ directory) is importable from this tests/ package.
"""
import os
import sys

_ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
)
if _ASSETS_DIR not in sys.path:
    sys.path.insert(0, _ASSETS_DIR)
