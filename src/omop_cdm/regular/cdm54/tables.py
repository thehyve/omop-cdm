"""OMOP CDM v5.4 tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, MetaData, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from omop_cdm import NAMING_CONVENTION
from omop_cdm.constants import (
    CDM_SCHEMA,
    FK_CARE_SITE_ID,
    FK_CONCEPT_CLASS_ID,
    FK_CONCEPT_ID,
    FK_DOMAIN_ID,
    FK_LOCATION_ID,
    FK_PERSON_ID,
    FK_PROVIDER_ID,
    FK_VISIT_DETAIL_ID,
    FK_VISIT_OCCURRENCE_ID,
    FK_VOCABULARY_ID,
    VOCAB_SCHEMA,
)
from omop_cdm.util import record_as_str


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Concept(Base):
    __tablename__ = "concept"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    concept_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    concept_name: Mapped[str] = mapped_column(String(255))
    domain_id: Mapped[str] = mapped_column(ForeignKey(FK_DOMAIN_ID), index=True)
    vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), index=True)
    concept_class_id: Mapped[str] = mapped_column(ForeignKey(FK_CONCEPT_CLASS_ID), index=True)
    standard_concept: Mapped[Optional[str]] = mapped_column(String(1))
    concept_code: Mapped[str] = mapped_column(String(50), index=True)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1))

    concept_class: Mapped["ConceptClass"] = relationship("ConceptClass", foreign_keys="Concept.concept_class_id")
    domain: Mapped["Domain"] = relationship("Domain", foreign_keys="Concept.domain_id")
    vocabulary: Mapped["Vocabulary"] = relationship("Vocabulary", foreign_keys="Concept.vocabulary_id")


class ConceptClass(Base):
    __tablename__ = "concept_class"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    concept_class_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    concept_class_name: Mapped[str] = mapped_column(String(255))
    concept_class_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    concept_class_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConceptClass.concept_class_concept_id"
    )


class Domain(Base):
    __tablename__ = "domain"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    domain_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    domain_name: Mapped[str] = mapped_column(String(255))
    domain_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    domain_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Domain.domain_concept_id")


class Vocabulary(Base):
    __tablename__ = "vocabulary"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    vocabulary_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    vocabulary_name: Mapped[str] = mapped_column(String(255))
    vocabulary_reference: Mapped[Optional[str]] = mapped_column(String(255))
    vocabulary_version: Mapped[Optional[str]] = mapped_column(String(255))
    vocabulary_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    vocabulary_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Vocabulary.vocabulary_concept_id")


class ConceptAncestor(Base):
    __tablename__ = "concept_ancestor"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    ancestor_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    descendant_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    min_levels_of_separation: Mapped[int] = mapped_column(Integer)
    max_levels_of_separation: Mapped[int] = mapped_column(Integer)

    ancestor_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="ConceptAncestor.ancestor_concept_id")
    descendant_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConceptAncestor.descendant_concept_id"
    )


class ConceptSynonym(Base):
    __tablename__ = "concept_synonym"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    concept_synonym_name: Mapped[str] = mapped_column(String(1000), primary_key=True)
    language_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True)

    concept: Mapped["Concept"] = relationship("Concept", foreign_keys="ConceptSynonym.concept_id")
    language_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="ConceptSynonym.language_concept_id")


class DrugStrength(Base):
    __tablename__ = "drug_strength"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    ingredient_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    amount_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    amount_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    numerator_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    numerator_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    denominator_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    denominator_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    box_size: Mapped[Optional[int]] = mapped_column(Integer)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1))

    amount_unit_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DrugStrength.amount_unit_concept_id"
    )
    denominator_unit_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DrugStrength.denominator_unit_concept_id"
    )
    drug_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugStrength.drug_concept_id")
    ingredient_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugStrength.ingredient_concept_id")
    numerator_unit_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DrugStrength.numerator_unit_concept_id"
    )


class Relationship(Base):
    __tablename__ = "relationship"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    relationship_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    relationship_name: Mapped[str] = mapped_column(String(255))
    is_hierarchical: Mapped[str] = mapped_column(String(1))
    defines_ancestry: Mapped[str] = mapped_column(String(1))
    reverse_relationship_id: Mapped[str] = mapped_column(ForeignKey(f"{VOCAB_SCHEMA}.relationship.relationship_id"))
    relationship_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    relationship_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Relationship.relationship_concept_id"
    )
    reverse_relationship: Mapped["Relationship"] = relationship(
        "Relationship", foreign_keys="Relationship.reverse_relationship_id"
    )


class ConceptRelationship(Base):
    __tablename__ = "concept_relationship"
    __table_args__ = {"schema": VOCAB_SCHEMA}
    __repr__ = record_as_str

    concept_id_1: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    concept_id_2: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey(f"{VOCAB_SCHEMA}.relationship.relationship_id"), primary_key=True, index=True
    )
    valid_start_date: Mapped[datetime.date] = mapped_column(Date)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1))

    concept_1: Mapped["Concept"] = relationship("Concept", foreign_keys="ConceptRelationship.concept_id_1")
    concept_2: Mapped["Concept"] = relationship("Concept", foreign_keys="ConceptRelationship.concept_id_2")
    relationship: Mapped["Relationship"] = relationship(
        "Relationship", foreign_keys="ConceptRelationship.relationship_id"
    )


class SourceToConceptMap(Base):
    __tablename__ = "source_to_concept_map"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    source_code: Mapped[str] = mapped_column(String(1000), primary_key=True, index=True)
    source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    source_vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), primary_key=True, index=True)
    source_code_description: Mapped[Optional[str]] = mapped_column(String(255))
    target_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    target_vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), index=True)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1))

    source_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="SourceToConceptMap.source_concept_id")
    source_vocabulary: Mapped["Vocabulary"] = relationship(
        "Vocabulary", foreign_keys="SourceToConceptMap.source_vocabulary_id"
    )
    target_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="SourceToConceptMap.target_concept_id")
    target_vocabulary: Mapped["Vocabulary"] = relationship(
        "Vocabulary", foreign_keys="SourceToConceptMap.target_vocabulary_id"
    )


class ConditionOccurrence(Base):
    __tablename__ = "condition_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    condition_occurrence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    condition_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    condition_start_date: Mapped[datetime.date] = mapped_column(Date)
    condition_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    condition_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    condition_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    condition_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    condition_status_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    stop_reason: Mapped[Optional[str]] = mapped_column(String(20))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    condition_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    condition_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    condition_status_source_value: Mapped[Optional[str]] = mapped_column(String(50))

    condition_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConditionOccurrence.condition_concept_id"
    )
    condition_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConditionOccurrence.condition_source_concept_id"
    )
    condition_status_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConditionOccurrence.condition_status_concept_id"
    )
    condition_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ConditionOccurrence.condition_type_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="ConditionOccurrence.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="ConditionOccurrence.provider_id")
    visit_detail: Mapped["VisitDetail"] = relationship(
        "VisitDetail", foreign_keys="ConditionOccurrence.visit_detail_id"
    )
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="ConditionOccurrence.visit_occurrence_id"
    )


class Death(Base):
    __tablename__ = "death"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), primary_key=True, index=True)
    death_date: Mapped[datetime.date] = mapped_column(Date)
    death_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    death_type_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    cause_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    cause_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    cause_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    cause_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Death.cause_concept_id")
    cause_source_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Death.cause_source_concept_id")
    death_type_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Death.death_type_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="Death.person_id")


class FactRelationship(Base):
    __tablename__ = "fact_relationship"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    domain_concept_id_1: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    fact_id_1: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain_concept_id_2: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)
    fact_id_2: Mapped[int] = mapped_column(Integer, primary_key=True)
    relationship_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True)

    domain_concept_1: Mapped["Concept"] = relationship("Concept", foreign_keys="FactRelationship.domain_concept_id_1")
    domain_concept_2: Mapped["Concept"] = relationship("Concept", foreign_keys="FactRelationship.domain_concept_id_2")
    relationship_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="FactRelationship.relationship_concept_id"
    )


class NoteNlp(Base):
    __tablename__ = "note_nlp"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    note_nlp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    note_id: Mapped[int] = mapped_column(Integer, index=True)
    section_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    snippet: Mapped[Optional[str]] = mapped_column(String(250))
    offset: Mapped[Optional[str]] = mapped_column(String(50))
    lexical_variant: Mapped[str] = mapped_column(String(250))
    note_nlp_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    note_nlp_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    nlp_system: Mapped[Optional[str]] = mapped_column(String(250))
    nlp_date: Mapped[datetime.date] = mapped_column(Date)
    nlp_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    term_exists: Mapped[Optional[str]] = mapped_column(String(1))
    term_temporal: Mapped[Optional[str]] = mapped_column(String(50))
    term_modifiers: Mapped[Optional[str]] = mapped_column(String(2000))

    note_nlp_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="NoteNlp.note_nlp_concept_id")
    note_nlp_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="NoteNlp.note_nlp_source_concept_id"
    )
    section_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="NoteNlp.section_concept_id")


class Person(Base):
    __tablename__ = "person"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    person_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    gender_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    year_of_birth: Mapped[int] = mapped_column(Integer)
    month_of_birth: Mapped[Optional[int]] = mapped_column(Integer)
    day_of_birth: Mapped[Optional[int]] = mapped_column(Integer)
    birth_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    race_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    ethnicity_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_LOCATION_ID))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID))
    person_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    gender_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    gender_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    race_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    race_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    ethnicity_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    ethnicity_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    care_site: Mapped["CareSite"] = relationship("CareSite", foreign_keys="Person.care_site_id")
    ethnicity_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Person.ethnicity_concept_id")
    ethnicity_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Person.ethnicity_source_concept_id"
    )
    gender_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Person.gender_concept_id")
    gender_source_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Person.gender_source_concept_id")
    location: Mapped["Location"] = relationship("Location", foreign_keys="Person.location_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="Person.provider_id")
    race_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Person.race_concept_id")
    race_source_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Person.race_source_concept_id")

    observation_periods: Mapped[list["ObservationPeriod"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    visit_occurrences: Mapped[list["VisitOccurrence"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    visit_details: Mapped[list["VisitDetail"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    condition_occurrences: Mapped[list["ConditionOccurrence"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    drug_exposures: Mapped[list["DrugExposure"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    procedure_occurrences: Mapped[list["ProcedureOccurrence"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    device_exposures: Mapped[list["DeviceExposure"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    observations: Mapped[list["Observation"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    death: Mapped["Death"] = relationship(back_populates="person", cascade="all, delete-orphan")
    notes: Mapped[list["Note"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    specimens: Mapped[list["Specimen"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    payer_plan_periods: Mapped[list["PayerPlanPeriod"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    drug_eras: Mapped[list["DrugEra"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    dose_eras: Mapped[list["DoseEra"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    condition_eras: Mapped[list["ConditionEra"]] = relationship(back_populates="person", cascade="all, delete-orphan")
    episodes: Mapped[list["Episode"]] = relationship(back_populates="person", cascade="all, delete-orphan")


class ObservationPeriod(Base):
    __tablename__ = "observation_period"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    observation_period_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    observation_period_start_date: Mapped[datetime.date] = mapped_column(Date)
    observation_period_end_date: Mapped[datetime.date] = mapped_column(Date)
    period_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    period_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ObservationPeriod.period_type_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="ObservationPeriod.person_id")


class Specimen(Base):
    __tablename__ = "specimen"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    specimen_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    specimen_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    specimen_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    specimen_date: Mapped[datetime.date] = mapped_column(Date)
    specimen_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    anatomic_site_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    disease_status_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    specimen_source_id: Mapped[Optional[str]] = mapped_column(String(50))
    specimen_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    anatomic_site_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    disease_status_source_value: Mapped[Optional[str]] = mapped_column(String(50))

    anatomic_site_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Specimen.anatomic_site_concept_id"
    )
    disease_status_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Specimen.disease_status_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="Specimen.person_id")
    specimen_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Specimen.specimen_concept_id")
    specimen_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Specimen.specimen_type_concept_id"
    )
    unit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Specimen.unit_concept_id")


class VisitOccurrence(Base):
    __tablename__ = "visit_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    visit_occurrence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    visit_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    visit_start_date: Mapped[datetime.date] = mapped_column(Date)
    visit_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    visit_end_date: Mapped[datetime.date] = mapped_column(Date)
    visit_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    visit_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID))
    visit_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    visit_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    admitted_from_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    admitted_from_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    discharged_to_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    discharged_to_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    preceding_visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID))

    admitted_from_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitOccurrence.admitted_from_concept_id"
    )
    care_site: Mapped["CareSite"] = relationship("CareSite", foreign_keys="VisitOccurrence.care_site_id")
    discharged_to_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitOccurrence.discharged_to_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="VisitOccurrence.person_id")
    preceding_visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="VisitOccurrence.preceding_visit_occurrence_id"
    )
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="VisitOccurrence.provider_id")
    visit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="VisitOccurrence.visit_concept_id")
    visit_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitOccurrence.visit_source_concept_id"
    )
    visit_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitOccurrence.visit_type_concept_id"
    )


class VisitDetail(Base):
    __tablename__ = "visit_detail"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    visit_detail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    visit_detail_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    visit_detail_start_date: Mapped[datetime.date] = mapped_column(Date)
    visit_detail_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    visit_detail_end_date: Mapped[datetime.date] = mapped_column(Date)
    visit_detail_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    visit_detail_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID))
    visit_detail_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    visit_detail_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    admitted_from_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    admitted_from_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    discharged_to_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    discharged_to_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    preceding_visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    parent_visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    visit_occurrence_id: Mapped[int] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)

    admitted_from_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitDetail.admitted_from_concept_id"
    )
    care_site: Mapped["CareSite"] = relationship("CareSite", foreign_keys="VisitDetail.care_site_id")
    discharged_to_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitDetail.discharged_to_concept_id"
    )
    parent_visit_detail: Mapped["VisitDetail"] = relationship(
        "VisitDetail", foreign_keys="VisitDetail.parent_visit_detail_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="VisitDetail.person_id")
    preceding_visit_detail: Mapped["VisitDetail"] = relationship(
        "VisitDetail", foreign_keys="VisitDetail.preceding_visit_detail_id"
    )
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="VisitDetail.provider_id")
    visit_detail_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitDetail.visit_detail_concept_id"
    )
    visit_detail_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitDetail.visit_detail_source_concept_id"
    )
    visit_detail_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="VisitDetail.visit_detail_type_concept_id"
    )
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="VisitDetail.visit_occurrence_id"
    )


class DeviceExposure(Base):
    __tablename__ = "device_exposure"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    device_exposure_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    device_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    device_exposure_start_date: Mapped[datetime.date] = mapped_column(Date)
    device_exposure_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    device_exposure_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    device_exposure_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    device_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unique_device_id: Mapped[Optional[str]] = mapped_column(String(255))
    production_id: Mapped[Optional[str]] = mapped_column(String(255))
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    device_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    device_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    unit_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    device_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DeviceExposure.device_concept_id")
    device_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DeviceExposure.device_source_concept_id"
    )
    device_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DeviceExposure.device_type_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="DeviceExposure.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="DeviceExposure.provider_id")
    unit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DeviceExposure.unit_concept_id")
    unit_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DeviceExposure.unit_source_concept_id"
    )
    visit_detail: Mapped["VisitDetail"] = relationship("VisitDetail", foreign_keys="DeviceExposure.visit_detail_id")
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="DeviceExposure.visit_occurrence_id"
    )


class DrugExposure(Base):
    __tablename__ = "drug_exposure"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    drug_exposure_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    drug_exposure_start_date: Mapped[datetime.date] = mapped_column(Date)
    drug_exposure_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    drug_exposure_end_date: Mapped[datetime.date] = mapped_column(Date)
    drug_exposure_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    verbatim_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    drug_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    stop_reason: Mapped[Optional[str]] = mapped_column(String(20))
    refills: Mapped[Optional[int]] = mapped_column(Integer)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    days_supply: Mapped[Optional[int]] = mapped_column(Integer)
    sig: Mapped[Optional[str]] = mapped_column(Text)
    route_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    lot_number: Mapped[Optional[str]] = mapped_column(String(50))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    drug_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    drug_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    route_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    dose_unit_source_value: Mapped[Optional[str]] = mapped_column(String(50))

    drug_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugExposure.drug_concept_id")
    drug_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="DrugExposure.drug_source_concept_id"
    )
    drug_type_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugExposure.drug_type_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="DrugExposure.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="DrugExposure.provider_id")
    route_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugExposure.route_concept_id")
    visit_detail: Mapped["VisitDetail"] = relationship("VisitDetail", foreign_keys="DrugExposure.visit_detail_id")
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="DrugExposure.visit_occurrence_id"
    )


class Measurement(Base):
    __tablename__ = "measurement"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    measurement_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    measurement_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    measurement_date: Mapped[datetime.date] = mapped_column(Date)
    measurement_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    measurement_time: Mapped[Optional[str]] = mapped_column(String(10))
    measurement_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    operator_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    range_low: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    range_high: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    measurement_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    measurement_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    unit_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    value_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    measurement_event_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    meas_event_field_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    meas_event_field_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Measurement.meas_event_field_concept_id"
    )
    measurement_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Measurement.measurement_concept_id")
    measurement_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Measurement.measurement_source_concept_id"
    )
    measurement_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Measurement.measurement_type_concept_id"
    )
    operator_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Measurement.operator_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="Measurement.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="Measurement.provider_id")
    unit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Measurement.unit_concept_id")
    unit_source_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Measurement.unit_source_concept_id")
    value_as_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Measurement.value_as_concept_id")
    visit_detail: Mapped["VisitDetail"] = relationship("VisitDetail", foreign_keys="Measurement.visit_detail_id")
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="Measurement.visit_occurrence_id"
    )


class Note(Base):
    __tablename__ = "note"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    note_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    note_date: Mapped[datetime.date] = mapped_column(Date)
    note_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    note_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    note_class_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    note_title: Mapped[Optional[str]] = mapped_column(String(250))
    note_text: Mapped[str] = mapped_column(Text)
    encoding_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    language_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    note_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    note_event_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    note_event_field_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    encoding_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Note.encoding_concept_id")
    language_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Note.language_concept_id")
    note_class_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Note.note_class_concept_id")
    note_event_field_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Note.note_event_field_concept_id"
    )
    note_type_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Note.note_type_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="Note.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="Note.provider_id")
    visit_detail: Mapped["VisitDetail"] = relationship("VisitDetail", foreign_keys="Note.visit_detail_id")
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="Note.visit_occurrence_id"
    )


class Observation(Base):
    __tablename__ = "observation"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    observation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    observation_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    observation_date: Mapped[datetime.date] = mapped_column(Date)
    observation_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    observation_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    value_as_string: Mapped[Optional[str]] = mapped_column(String(60))
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    qualifier_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    observation_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    observation_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    qualifier_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    value_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    observation_event_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    obs_event_field_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    obs_event_field_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Observation.obs_event_field_concept_id"
    )
    observation_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Observation.observation_concept_id")
    observation_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Observation.observation_source_concept_id"
    )
    observation_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Observation.observation_type_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="Observation.person_id")
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="Observation.provider_id")
    qualifier_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Observation.qualifier_concept_id")
    unit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Observation.unit_concept_id")
    value_as_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Observation.value_as_concept_id")
    visit_detail: Mapped["VisitDetail"] = relationship("VisitDetail", foreign_keys="Observation.visit_detail_id")
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="Observation.visit_occurrence_id"
    )


class ProcedureOccurrence(Base):
    __tablename__ = "procedure_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    procedure_occurrence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    procedure_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    procedure_date: Mapped[datetime.date] = mapped_column(Date)
    procedure_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    procedure_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    procedure_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    procedure_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    modifier_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID))
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID))
    procedure_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    procedure_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    modifier_source_value: Mapped[Optional[str]] = mapped_column(String(50))

    modifier_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ProcedureOccurrence.modifier_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="ProcedureOccurrence.person_id")
    procedure_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ProcedureOccurrence.procedure_concept_id"
    )
    procedure_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ProcedureOccurrence.procedure_source_concept_id"
    )
    procedure_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="ProcedureOccurrence.procedure_type_concept_id"
    )
    provider: Mapped["Provider"] = relationship("Provider", foreign_keys="ProcedureOccurrence.provider_id")
    visit_detail: Mapped["VisitDetail"] = relationship(
        "VisitDetail", foreign_keys="ProcedureOccurrence.visit_detail_id"
    )
    visit_occurrence: Mapped["VisitOccurrence"] = relationship(
        "VisitOccurrence", foreign_keys="ProcedureOccurrence.visit_occurrence_id"
    )


class ConditionEra(Base):
    __tablename__ = "condition_era"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    condition_era_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    condition_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    condition_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    condition_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    condition_occurrence_count: Mapped[Optional[int]] = mapped_column(Integer)

    condition_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="ConditionEra.condition_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="ConditionEra.person_id")


class DoseEra(Base):
    __tablename__ = "dose_era"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    dose_era_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    unit_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    dose_value: Mapped[decimal.Decimal] = mapped_column(Numeric)
    dose_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    dose_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    drug_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DoseEra.drug_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="DoseEra.person_id")
    unit_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DoseEra.unit_concept_id")


class DrugEra(Base):
    __tablename__ = "drug_era"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    drug_era_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    drug_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    drug_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    drug_exposure_count: Mapped[Optional[int]] = mapped_column(Integer)
    gap_days: Mapped[Optional[int]] = mapped_column(Integer)

    drug_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="DrugEra.drug_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="DrugEra.person_id")


class Episode(Base):
    __tablename__ = "episode"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    episode_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"))
    episode_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    episode_start_date: Mapped[datetime.date] = mapped_column(Date)
    episode_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    episode_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    episode_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    episode_parent_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    episode_number: Mapped[Optional[int]] = mapped_column(Integer)
    episode_object_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    episode_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    episode_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    episode_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    episode_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Episode.episode_concept_id")
    episode_object_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Episode.episode_object_concept_id"
    )
    episode_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Episode.episode_source_concept_id"
    )
    episode_type_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Episode.episode_type_concept_id")
    person: Mapped["Person"] = relationship("Person", foreign_keys="Episode.person_id")


class EpisodeEvent(Base):
    __tablename__ = "episode_event"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    episode_id: Mapped[int] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.episode.episode_id", ondelete="CASCADE"), primary_key=True
    )
    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    episode_event_field_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True)

    episode_event_field_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="EpisodeEvent.episode_event_field_concept_id"
    )
    episode: Mapped["Episode"] = relationship("Episode", foreign_keys="EpisodeEvent.episode_id")


class PayerPlanPeriod(Base):
    __tablename__ = "payer_plan_period"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    payer_plan_period_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID, ondelete="CASCADE"), index=True)
    payer_plan_period_start_date: Mapped[datetime.date] = mapped_column(Date)
    payer_plan_period_end_date: Mapped[datetime.date] = mapped_column(Date)
    payer_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    payer_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    payer_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    plan_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    plan_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    plan_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    sponsor_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    sponsor_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    sponsor_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    family_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    stop_reason_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    stop_reason_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    stop_reason_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    payer_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="PayerPlanPeriod.payer_concept_id")
    payer_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="PayerPlanPeriod.payer_source_concept_id"
    )
    person: Mapped["Person"] = relationship("Person", foreign_keys="PayerPlanPeriod.person_id")
    plan_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="PayerPlanPeriod.plan_concept_id")
    plan_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="PayerPlanPeriod.plan_source_concept_id"
    )
    sponsor_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="PayerPlanPeriod.sponsor_concept_id")
    sponsor_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="PayerPlanPeriod.sponsor_source_concept_id"
    )
    stop_reason_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="PayerPlanPeriod.stop_reason_concept_id"
    )
    stop_reason_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="PayerPlanPeriod.stop_reason_source_concept_id"
    )


class Cost(Base):
    __tablename__ = "cost"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    cost_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost_event_id: Mapped[int] = mapped_column(Integer, index=True)
    cost_domain_id: Mapped[str] = mapped_column(ForeignKey(FK_DOMAIN_ID))
    cost_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    currency_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    total_charge: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    total_cost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    total_paid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_by_payer: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_by_patient: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_patient_copay: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_patient_coinsurance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_patient_deductible: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_by_primary: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_ingredient_cost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    paid_dispensing_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    payer_plan_period_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.payer_plan_period.payer_plan_period_id")
    )
    amount_allowed: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    revenue_code_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    revenue_code_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    drg_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    drg_source_value: Mapped[Optional[str]] = mapped_column(String(3))

    cost_domain: Mapped["Domain"] = relationship("Domain", foreign_keys="Cost.cost_domain_id")
    cost_type_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Cost.cost_type_concept_id")
    currency_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Cost.currency_concept_id")
    drg_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Cost.drg_concept_id")
    revenue_code_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Cost.revenue_code_concept_id")


class CareSite(Base):
    __tablename__ = "care_site"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    care_site_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    care_site_name: Mapped[Optional[str]] = mapped_column(String(255))
    place_of_service_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_LOCATION_ID))
    care_site_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    place_of_service_source_value: Mapped[Optional[str]] = mapped_column(String(50))

    location: Mapped["Location"] = relationship("Location", foreign_keys="CareSite.location_id")
    place_of_service_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="CareSite.place_of_service_concept_id"
    )


class Location(Base):
    __tablename__ = "location"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address_1: Mapped[Optional[str]] = mapped_column(String(50))
    address_2: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    state: Mapped[Optional[str]] = mapped_column(String(2))
    zip: Mapped[Optional[str]] = mapped_column(String(9))
    county: Mapped[Optional[str]] = mapped_column(String(20))
    location_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    country_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    country_source_value: Mapped[Optional[str]] = mapped_column(String(80))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)

    country_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Location.country_concept_id")


class Provider(Base):
    __tablename__ = "provider"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    provider_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255))
    npi: Mapped[Optional[str]] = mapped_column(String(20))
    dea: Mapped[Optional[str]] = mapped_column(String(20))
    specialty_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID))
    year_of_birth: Mapped[Optional[int]] = mapped_column(Integer)
    gender_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    provider_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    specialty_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    specialty_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    gender_source_value: Mapped[Optional[str]] = mapped_column(String(50))
    gender_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))

    care_site: Mapped["CareSite"] = relationship("CareSite", foreign_keys="Provider.care_site_id")
    gender_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Provider.gender_concept_id")
    gender_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Provider.gender_source_concept_id"
    )
    specialty_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Provider.specialty_concept_id")
    specialty_source_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Provider.specialty_source_concept_id"
    )


class CdmSource(Base):
    __tablename__ = "cdm_source"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    cdm_source_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    cdm_source_abbreviation: Mapped[str] = mapped_column(String(25))
    cdm_holder: Mapped[str] = mapped_column(String(255))
    source_description: Mapped[Optional[str]] = mapped_column(Text)
    source_documentation_reference: Mapped[Optional[str]] = mapped_column(String(255))
    cdm_etl_reference: Mapped[Optional[str]] = mapped_column(String(255))
    source_release_date: Mapped[datetime.date] = mapped_column(Date)
    cdm_release_date: Mapped[datetime.date] = mapped_column(Date)
    cdm_version: Mapped[Optional[str]] = mapped_column(String(10))
    cdm_version_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    vocabulary_version: Mapped[str] = mapped_column(String(20))

    cdm_version_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="CdmSource.cdm_version_concept_id")


class Metadata(Base):
    __tablename__ = "metadata"
    __table_args__ = {"schema": CDM_SCHEMA}
    __repr__ = record_as_str

    metadata_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    metadata_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True)
    metadata_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    name: Mapped[str] = mapped_column(String(250))
    value_as_string: Mapped[Optional[str]] = mapped_column(String(250))
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID))
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    metadata_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    metadata_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    metadata_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Metadata.metadata_concept_id")
    metadata_type_concept: Mapped["Concept"] = relationship(
        "Concept", foreign_keys="Metadata.metadata_type_concept_id"
    )
    value_as_concept: Mapped["Concept"] = relationship("Concept", foreign_keys="Metadata.value_as_concept_id")
