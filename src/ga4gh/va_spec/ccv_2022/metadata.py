"""Provide metadata for CCV 2022 VA-Spec models."""

from ga4gh.va_spec.metadata import VASpecMetadataMixin


class CCV2022MetadataMixin(VASpecMetadataMixin):
    """Provide metadata shared by models in the CCV 2022 namespace."""

    _schema_namespace = "ccv-2022"
