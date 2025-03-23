"""Shared enums"""

from enum import Enum


class StrengthOfEvidenceProvided(str, Enum):
    """Define constraints for strength of evidence provided values"""

    STANDALONE = "standalone"
    VERY_STRONG = "very strong"
    STRONG = "strong"
    MODERATE = "moderate"
    SUPPORTING = "supporting"


STRENGTH_OF_EVIDENCE_PROVIDED_VALUES = [
    v.value for v in StrengthOfEvidenceProvided.__members__.values()
]


class Strength(str, Enum):
    """Define constrains for strength"""

    DEFINITIVE = "definitive"
    LIKELY = "likely"


STRENGTHS = [v.value for v in Strength.__members__.values()]


class System(str, Enum):
    """Define constraints for systems"""

    ACMG = "ACMG Guidelines, 2015"
    AMP_ASCO_CAP = "AMP/ASCO/CAP (AAC) Guidelines, 2017"
    CLIN_GEN = "ClinGen Low Penetrance and Risk Allele Recommendations, 2024"
    CCV = "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022"
