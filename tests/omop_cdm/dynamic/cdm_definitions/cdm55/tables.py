from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.omop_cdm.constants import NAMING_CONVENTION
from src.omop_cdm.dynamic.cdm55.clinical_data import (
    BaseConditionOccurrenceCdm55,
    BaseDeathCdm55,
    BaseDeviceExposureCdm55,
    BaseDrugExposureCdm55,
    BaseFactRelationshipCdm55,
    BaseMeasurementCdm55,
    BaseNoteCdm55,
    BaseNoteNlpCdm55,
    BaseObservationCdm55,
    BaseObservationPeriodCdm55,
    BasePersonCdm55,
    BaseProcedureOccurrenceCdm55,
    BaseSpecimenCdm55,
    BaseStemTableCdm55,
    BaseVisitDetailCdm55,
    BaseVisitOccurrenceCdm55,
)
from src.omop_cdm.dynamic.cdm55.derived_elements import (
    BaseConditionEraCdm55,
    BaseDoseEraCdm55,
    BaseDrugEraCdm55,
    BaseEpisodeCdm55,
    BaseEpisodeEventCdm55,
)
from src.omop_cdm.dynamic.cdm55.health_economics import (
    BaseCostCdm55,
    BasePayerPlanPeriodCdm55,
)
from src.omop_cdm.dynamic.cdm55.health_system_data import (
    BaseCareSiteCdm55,
    BaseLocationCdm55,
    BaseProviderCdm55,
)
from src.omop_cdm.dynamic.cdm55.metadata import (
    BaseCdmSourceCdm55,
    BaseMetadataCdm55,
)
from src.omop_cdm.dynamic.cdm55.vocabularies.vocabularies import (
    BaseConceptAncestorCdm55,
    BaseConceptCdm55,
    BaseConceptClassCdm55,
    BaseConceptMetadataCdm55,
    BaseConceptRelationshipMetadataCdm55,
    BaseConceptRelationshipCdm55,
    BaseConceptSynonymCdm55,
    BaseDomainCdm55,
    BaseDrugStrengthCdm55,
    BasePackContentCdm55,
    BaseRelationshipCdm55,
    BaseSourceToConceptMapCdm55,
    BaseSourceToConceptMapVersionCdm55,
    BaseVocabularyCdm55,
)


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Person(BasePersonCdm55, Base):
    pass


class Death(BaseDeathCdm55, Base):
    pass


class Note(BaseNoteCdm55, Base):
    pass


class Measurement(BaseMeasurementCdm55, Base):
    pass


class NoteNlp(BaseNoteNlpCdm55, Base):
    pass


class Observation(BaseObservationCdm55, Base):
    pass


class Specimen(BaseSpecimenCdm55, Base):
    pass


class StemTable(BaseStemTableCdm55, Base):
    pass


class VisitDetail(BaseVisitDetailCdm55, Base):
    pass


class ConditionOccurrence(BaseConditionOccurrenceCdm55, Base):
    pass


class DeviceExposure(BaseDeviceExposureCdm55, Base):
    pass


class DrugExposure(BaseDrugExposureCdm55, Base):
    pass


class FactRelationship(BaseFactRelationshipCdm55, Base):
    pass


class ObservationPeriod(BaseObservationPeriodCdm55, Base):
    pass


class ProcedureOccurrence(BaseProcedureOccurrenceCdm55, Base):
    pass


class VisitOccurrence(BaseVisitOccurrenceCdm55, Base):
    pass


class Location(BaseLocationCdm55, Base):
    pass


class CareSite(BaseCareSiteCdm55, Base):
    pass


class Provider(BaseProviderCdm55, Base):
    pass


class Cost(BaseCostCdm55, Base):
    pass


class PayerPlanPeriod(BasePayerPlanPeriodCdm55, Base):
    pass


class DoseEra(BaseDoseEraCdm55, Base):
    pass


class DrugEra(BaseDrugEraCdm55, Base):
    pass


class ConditionEra(BaseConditionEraCdm55, Base):
    pass


class Episode(BaseEpisodeCdm55, Base):
    pass


class EpisodeEvent(BaseEpisodeEventCdm55, Base):
    pass


class CdmSource(BaseCdmSourceCdm55, Base):
    pass


class Metadata(BaseMetadataCdm55, Base):
    pass


class Concept(BaseConceptCdm55, Base):
    pass


class ConceptAncestor(BaseConceptAncestorCdm55, Base):
    pass


class ConceptClass(BaseConceptClassCdm55, Base):
    pass


class ConceptRelationship(BaseConceptRelationshipCdm55, Base):
    pass


class ConceptSynonym(BaseConceptSynonymCdm55, Base):
    pass


class DrugStrength(BaseDrugStrengthCdm55, Base):
    pass


class Relationship(BaseRelationshipCdm55, Base):
    pass


class SourceToConceptMap(BaseSourceToConceptMapCdm55, Base):
    pass


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm55, Base):
    pass


class Vocabulary(BaseVocabularyCdm55, Base):
    pass


class Domain(BaseDomainCdm55, Base):
    pass

class PackContent(BasePackContentCdm55, Base):
    pass

class ConceptMetadata(BaseConceptMetadataCdm55, Base):
    pass

class ConceptRelationshipMetadata(BaseConceptRelationshipMetadataCdm55, Base):
    pass