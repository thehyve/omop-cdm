from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.omop_cdm.constants import NAMING_CONVENTION
from src.omop_cdm.dynamic.cdm54.clinical_data import (
    BaseConditionOccurrenceCdm54,
    BaseDeathCdm54,
    BaseDeviceExposureCdm54,
    BaseDrugExposureCdm54,
    BaseFactRelationshipCdm54,
    BaseMeasurementCdm54,
    BaseNoteCdm54,
    BaseNoteNlpCdm54,
    BaseObservationCdm54,
    BaseObservationPeriodCdm54,
    BasePersonCdm54,
    BaseProcedureOccurrenceCdm54,
    BaseSpecimenCdm54,
    BaseStemTableCdm54,
    BaseVisitDetailCdm54,
    BaseVisitOccurrenceCdm54,
)
from src.omop_cdm.dynamic.cdm54.derived_elements import (
    BaseConditionEraCdm54,
    BaseDoseEraCdm54,
    BaseDrugEraCdm54,
    BaseEpisodeCdm54,
    BaseEpisodeEventCdm54,
)
from src.omop_cdm.dynamic.cdm54.health_economics import (
    BaseCostCdm54,
    BasePayerPlanPeriodCdm54,
)
from src.omop_cdm.dynamic.cdm54.health_system_data import (
    BaseCareSiteCdm54,
    BaseLocationCdm54,
    BaseProviderCdm54,
)
from src.omop_cdm.dynamic.cdm54.metadata import (
    BaseCdmSourceCdm54,
    BaseMetadataCdm54,
)
from src.omop_cdm.dynamic.cdm54.vocabularies.vocabularies import (
    BaseConceptAncestorCdm54,
    BaseConceptCdm54,
    BaseConceptClassCdm54,
    BaseConceptRelationshipCdm54,
    BaseConceptSynonymCdm54,
    BaseDomainCdm54,
    BaseDrugStrengthCdm54,
    BaseRelationshipCdm54,
    BaseSourceToConceptMapCdm54,
    BaseSourceToConceptMapVersionCdm54,
    BaseVocabularyCdm54,
)
from src.omop_cdm.dynamic.legacy.legacy import (
    BaseAttributeDefinition,
    BaseCohort,
    BaseCohortAttribute,
    BaseCohortDefinition,
)


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Person(BasePersonCdm54, Base):
    pass


class Death(BaseDeathCdm54, Base):
    pass


class Note(BaseNoteCdm54, Base):
    pass


class Measurement(BaseMeasurementCdm54, Base):
    pass


class NoteNlp(BaseNoteNlpCdm54, Base):
    pass


class Observation(BaseObservationCdm54, Base):
    pass


class Specimen(BaseSpecimenCdm54, Base):
    pass


class StemTable(BaseStemTableCdm54, Base):
    pass


class VisitDetail(BaseVisitDetailCdm54, Base):
    pass


class ConditionOccurrence(BaseConditionOccurrenceCdm54, Base):
    pass


class DeviceExposure(BaseDeviceExposureCdm54, Base):
    pass


class DrugExposure(BaseDrugExposureCdm54, Base):
    pass


class FactRelationship(BaseFactRelationshipCdm54, Base):
    pass


class ObservationPeriod(BaseObservationPeriodCdm54, Base):
    pass


class ProcedureOccurrence(BaseProcedureOccurrenceCdm54, Base):
    pass


class VisitOccurrence(BaseVisitOccurrenceCdm54, Base):
    pass


class Location(BaseLocationCdm54, Base):
    pass


class CareSite(BaseCareSiteCdm54, Base):
    pass


class Provider(BaseProviderCdm54, Base):
    pass


class Cost(BaseCostCdm54, Base):
    pass


class PayerPlanPeriod(BasePayerPlanPeriodCdm54, Base):
    pass


class DoseEra(BaseDoseEraCdm54, Base):
    pass


class DrugEra(BaseDrugEraCdm54, Base):
    pass


class ConditionEra(BaseConditionEraCdm54, Base):
    pass


class Episode(BaseEpisodeCdm54, Base):
    pass


class EpisodeEvent(BaseEpisodeEventCdm54, Base):
    pass


class CdmSource(BaseCdmSourceCdm54, Base):
    pass


class Metadata(BaseMetadataCdm54, Base):
    pass


class Concept(BaseConceptCdm54, Base):
    pass


class ConceptAncestor(BaseConceptAncestorCdm54, Base):
    pass


class ConceptClass(BaseConceptClassCdm54, Base):
    pass


class ConceptRelationship(BaseConceptRelationshipCdm54, Base):
    pass


class ConceptSynonym(BaseConceptSynonymCdm54, Base):
    pass


class DrugStrength(BaseDrugStrengthCdm54, Base):
    pass


class Relationship(BaseRelationshipCdm54, Base):
    pass


class SourceToConceptMap(BaseSourceToConceptMapCdm54, Base):
    pass


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm54, Base):
    pass


class Vocabulary(BaseVocabularyCdm54, Base):
    pass


class Domain(BaseDomainCdm54, Base):
    pass


class Cohort(BaseCohort, Base):
    pass


class CohortAttribute(BaseCohortAttribute, Base):
    pass


class CohortDefinition(BaseCohortDefinition, Base):
    pass


class AttributeDefinition(BaseAttributeDefinition, Base):
    pass
