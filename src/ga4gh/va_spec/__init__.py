"""Package for VA-Spec Python implementation"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

from ga4gh.va_spec.version import VASPEC_VERSION

try:
    __version__ = package_version(__name__)
except PackageNotFoundError:  # pragma: nocover
    __version__ = "unknown"
finally:
    del package_version, PackageNotFoundError

__all__ = ["VASPEC_VERSION", "__version__"]
