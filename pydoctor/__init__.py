"""PyDoctor, an API documentation generator for Python libraries."""

__all__ = ["__version__"]

from ._version import __version__


def _setuptools_version():
    return __version__.public()
