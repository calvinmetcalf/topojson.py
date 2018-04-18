from .conversion import convert as topojson
from .geojson import geojson

_all_ = ['geojson', 'topojson']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
