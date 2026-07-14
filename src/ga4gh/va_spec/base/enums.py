"""Shared enums"""

from enum import Enum


class DiagnosticPredicate(str, Enum):
    """Define constraints for diagnostic predicate"""

    INCLUSIVE = "isDiagnosticInclusionCriterionFor"
    EXCLUSIVE = "isDiagnosticExclusionCriterionFor"


class PrognosticPredicate(str, Enum):
    """Define constraints for prognostic predicate"""

    BETTER_OUTCOME = "associatedWithBetterOutcomeFor"
    WORSE_OUTCOME = "associatedWithWorseOutcomeFor"


class TherapeuticResponsePredicate(str, Enum):
    """Define constraints for therapeutic response predicate"""

    SENSITIVITY = "predictsSensitivityTo"
    RESISTANCE = "predictsResistanceTo"


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


class StrengthCode(str, Enum):
    """Define constrains for strength

    Used in ACMG 2015 and CCV 2022
    """

    DEFINITIVE = "definitive"
    LIKELY = "likely"


STRENGTH_CODES = [v.value for v in StrengthCode.__members__.values()]


class ClinGenClassification(str, Enum):
    """Define constraints for ClinGen classifications"""

    PATHOGENIC_LOW_PEN = "pathogenic, low penetrance"
    LIKELY_PATHOGENIC_LOW_PEN = "likely pathogenic, low penetrance"
    ESTABLISHED_RISK_ALLELE = "established risk allele"
    LIKELY_RISK_ALLELE = "likely risk allele"
    UNCERTAIN_RISK_ALLELE = "uncertain risk allele"


CLIN_GEN_CLASSIFICATIONS = [v.value for v in ClinGenClassification.__members__.values()]


class CcvClassification(str, Enum):
    """Define constraints for CCV classifications"""

    ONCOGENIC = "oncogenic"
    LIKELY_ONCOGENIC = "likely oncogenic"
    UNCERTAIN_SIGNIFICANCE = "uncertain significance"
    LIKELY_BENIGN = "likely benign"
    BENIGN = "benign"


CCV_CLASSIFICATIONS = [v.value for v in CcvClassification.__members__.values()]


class System(str, Enum):
    """Define constraints for systems"""

    ACMG = "ACMG Guidelines, 2015"
    AMP_ASCO_CAP = "AMP/ASCO/CAP Guidelines, 2017"
    CLIN_GEN = "ClinGen Low Penetrance and Risk Allele Recommendations, 2024"
    CCV = "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022"
