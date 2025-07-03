"""Package for VA-Spec Python implementation"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: nocover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


VASPEC_VERSION = "1.0.0"
