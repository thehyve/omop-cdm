from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from omop_cdm.constants import NAMING_CONVENTION

from omop_cdm.dynamic.cdm600.clinical_data import (
    BasePersonCdm600,
    BaseNoteCdm600,
    BaseMeasurementCdm600,
    BaseNoteNlpCdm600,
    BaseObservationCdm600,
    BaseSpecimenCdm600,
    BaseStemTableCdm600,
    BaseVisitDetailCdm600,
    BaseConditionOccurrenceCdm600,
    BaseDeviceExposureCdm600,
    BaseDrugExposureCdm600,
    BaseFactRelationshipCdm600,
    BaseObservationPeriodCdm600,
    BaseProcedureOccurrenceCdm600,
    BaseSurveyConductCdm600,
    BaseVisitOccurrenceCdm600,
)

from omop_cdm.dynamic.cdm600.health_system_data import (
    BaseCareSiteCdm600,
    BaseLocationCdm600,
    BaseProviderCdm600,
    BaseLocationHistoryCdm600,
)

from omop_cdm.dynamic.cdm600.health_economics import (
    BaseCostCdm600,
    BasePayerPlanPeriodCdm600,
)

from omop_cdm.dynamic.cdm600.derived_elements import (
    BaseDoseEraCdm600,
    BaseDrugEraCdm600,
    BaseConditionEraCdm600,
)

from omop_cdm.dynamic.cdm600.metadata import (
    BaseMetadataCdm600,
    BaseCdmSourceCdm600,
)

from omop_cdm.dynamic.cdm600.vocabularies import (
    BaseVocabularyCdm600,
    BaseSourceToConceptMapCdm600,
    BaseSourceToConceptMapVersionCdm600,
    BaseConceptCdm600,
    BaseConceptAncestorCdm600,
    BaseConceptClassCdm600,
    BaseConceptRelationshipCdm600,
    BaseConceptSynonymCdm600,
    BaseDomainCdm600,
    BaseDrugStrengthCdm600,
    BaseRelationshipCdm600,
)


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Person(BasePersonCdm600, Base):
    pass


class Note(BaseNoteCdm600, Base):
    pass


class Measurement(BaseMeasurementCdm600, Base):
    pass


class NoteNlp(BaseNoteNlpCdm600, Base):
    pass


class Observation(BaseObservationCdm600, Base):
    pass


class Specimen(BaseSpecimenCdm600, Base):
    pass


class StemTable(BaseStemTableCdm600, Base):
    pass


class VisitDetail(BaseVisitDetailCdm600, Base):
    pass


class ConditionOccurrence(BaseConditionOccurrenceCdm600, Base):
    pass


class DeviceExposure(BaseDeviceExposureCdm600, Base):
    pass


class DrugExposure(BaseDrugExposureCdm600, Base):
    pass


class FactRelationship(BaseFactRelationshipCdm600, Base):
    pass


class ObservationPeriod(BaseObservationPeriodCdm600, Base):
    pass


class ProcedureOccurrence(BaseProcedureOccurrenceCdm600, Base):
    pass


class SurveyConduct(BaseSurveyConductCdm600, Base):
    pass


class VisitOccurrence(BaseVisitOccurrenceCdm600, Base):
    pass


class Cost(BaseCostCdm600, Base):
    pass


class PayerPlanPeriod(BasePayerPlanPeriodCdm600, Base):
    pass


class CdmSource(BaseCdmSourceCdm600, Base):
    pass


class Metadata(BaseMetadataCdm600, Base):
    pass


class DoseEra(BaseDoseEraCdm600, Base):
    pass


class DrugEra(BaseDrugEraCdm600, Base):
    pass


class ConditionEra(BaseConditionEraCdm600, Base):
    pass


class Location(BaseLocationCdm600, Base):
    pass


class CareSite(BaseCareSiteCdm600, Base):
    pass


class Provider(BaseProviderCdm600, Base):
    pass


class LocationHistory(BaseLocationHistoryCdm600, Base):
    pass


class Concept(BaseConceptCdm600, Base):
    pass


class ConceptAncestor(BaseConceptAncestorCdm600, Base):
    pass


class ConceptClass(BaseConceptClassCdm600, Base):
    pass


class ConceptRelationship(BaseConceptRelationshipCdm600, Base):
    pass


class ConceptSynonym(BaseConceptSynonymCdm600, Base):
    pass


class DrugStrength(BaseDrugStrengthCdm600, Base):
    pass


class Relationship(BaseRelationshipCdm600, Base):
    pass


class SourceToConceptMap(BaseSourceToConceptMapCdm600, Base):
    pass


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm600, Base):
    pass


class Vocabulary(BaseVocabularyCdm600, Base):
    pass


class Domain(BaseDomainCdm600, Base):
    pass
