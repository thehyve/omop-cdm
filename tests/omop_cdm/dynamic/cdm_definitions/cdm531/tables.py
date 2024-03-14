from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.omop_cdm.constants import NAMING_CONVENTION
from src.omop_cdm.dynamic.cdm531.clinical_data import (
    BaseConditionOccurrenceCdm531,
    BaseDeathCdm531,
    BaseDeviceExposureCdm531,
    BaseDrugExposureCdm531,
    BaseFactRelationshipCdm531,
    BaseMeasurementCdm531,
    BaseNoteCdm531,
    BaseNoteNlpCdm531,
    BaseObservationCdm531,
    BaseObservationPeriodCdm531,
    BasePersonCdm531,
    BaseProcedureOccurrenceCdm531,
    BaseSpecimenCdm531,
    BaseStemTableCdm531,
    BaseVisitDetailCdm531,
    BaseVisitOccurrenceCdm531,
)
from src.omop_cdm.dynamic.cdm531.derived_elements import (
    BaseConditionEraCdm531,
    BaseDoseEraCdm531,
    BaseDrugEraCdm531,
)
from src.omop_cdm.dynamic.cdm531.health_economics import (
    BaseCostCdm531,
    BasePayerPlanPeriodCdm531,
)
from src.omop_cdm.dynamic.cdm531.health_system_data import (
    BaseCareSiteCdm531,
    BaseLocationCdm531,
    BaseProviderCdm531,
)
from src.omop_cdm.dynamic.cdm531.metadata import (
    BaseCdmSourceCdm531,
    BaseMetadataCdm531,
)
from src.omop_cdm.dynamic.cdm531.vocabularies import (
    BaseConceptAncestorCdm531,
    BaseConceptCdm531,
    BaseConceptClassCdm531,
    BaseConceptRelationshipCdm531,
    BaseConceptSynonymCdm531,
    BaseDomainCdm531,
    BaseDrugStrengthCdm531,
    BaseRelationshipCdm531,
    BaseSourceToConceptMapCdm531,
    BaseSourceToConceptMapVersionCdm531,
    BaseVocabularyCdm531,
)


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Person(BasePersonCdm531, Base):
    pass


class Death(BaseDeathCdm531, Base):
    pass


class Note(BaseNoteCdm531, Base):
    pass


class Measurement(BaseMeasurementCdm531, Base):
    pass


class NoteNlp(BaseNoteNlpCdm531, Base):
    pass


class Observation(BaseObservationCdm531, Base):
    pass


class Specimen(BaseSpecimenCdm531, Base):
    pass


class StemTable(BaseStemTableCdm531, Base):
    pass


class VisitDetail(BaseVisitDetailCdm531, Base):
    pass


class ConditionOccurrence(BaseConditionOccurrenceCdm531, Base):
    pass


class DeviceExposure(BaseDeviceExposureCdm531, Base):
    pass


class DrugExposure(BaseDrugExposureCdm531, Base):
    pass


class FactRelationship(BaseFactRelationshipCdm531, Base):
    pass


class ObservationPeriod(BaseObservationPeriodCdm531, Base):
    pass


class ProcedureOccurrence(BaseProcedureOccurrenceCdm531, Base):
    pass


class VisitOccurrence(BaseVisitOccurrenceCdm531, Base):
    pass


class Location(BaseLocationCdm531, Base):
    pass


class CareSite(BaseCareSiteCdm531, Base):
    pass


class Provider(BaseProviderCdm531, Base):
    pass


class Cost(BaseCostCdm531, Base):
    pass


class PayerPlanPeriod(BasePayerPlanPeriodCdm531, Base):
    pass


class DoseEra(BaseDoseEraCdm531, Base):
    pass


class DrugEra(BaseDrugEraCdm531, Base):
    pass


class ConditionEra(BaseConditionEraCdm531, Base):
    pass


class CdmSource(BaseCdmSourceCdm531, Base):
    pass


class Metadata(BaseMetadataCdm531, Base):
    pass


class Concept(BaseConceptCdm531, Base):
    pass


class ConceptAncestor(BaseConceptAncestorCdm531, Base):
    pass


class ConceptClass(BaseConceptClassCdm531, Base):
    pass


class ConceptRelationship(BaseConceptRelationshipCdm531, Base):
    pass


class ConceptSynonym(BaseConceptSynonymCdm531, Base):
    pass


class DrugStrength(BaseDrugStrengthCdm531, Base):
    pass


class Relationship(BaseRelationshipCdm531, Base):
    pass


class SourceToConceptMap(BaseSourceToConceptMapCdm531, Base):
    pass


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm531, Base):
    pass


class Vocabulary(BaseVocabularyCdm531, Base):
    pass


class Domain(BaseDomainCdm531, Base):
    pass
