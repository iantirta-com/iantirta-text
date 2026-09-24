# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from importlib.metadata import version

from .filter import filter_text
from .normalize import normalize
from .romanize import romanize

__all__ = [
    "normalize",
    "filter_text",
    "romanize",
]

__version__ = version("iantirta-text")