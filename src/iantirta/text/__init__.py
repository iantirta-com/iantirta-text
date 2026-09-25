# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from importlib.metadata import version

from .alignment import Alignment, align, distance, similarity
from .filter import filter_text
from .normalize import normalize
from .romanize import romanize

__all__ = [
    "normalize",
    "filter_text",
    "romanize",
    "Alignment",
    "align",
    "distance",
    "similarity",
]

__version__ = version("iantirta-text")