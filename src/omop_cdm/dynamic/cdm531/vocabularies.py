"""OMOP CDM v5.3.1 vocabulary tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omop_cdm.constants import (
    CDM_SCHEMA,
    FK_CONCEPT_CLASS_ID,
    FK_CONCEPT_ID,
    FK_DOMAIN_ID,
    FK_VOCABULARY_ID,
    VOCAB_SCHEMA,
)


class BaseConceptCdm531:
    __tablename__ = "concept"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    concept_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    concept_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    domain_id: Mapped[str] = mapped_column(ForeignKey(FK_DOMAIN_ID), index=True, sort_order=300)
    vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), index=True, sort_order=400)
    concept_class_id: Mapped[str] = mapped_column(ForeignKey(FK_CONCEPT_CLASS_ID), index=True, sort_order=500)
    standard_concept: Mapped[Optional[str]] = mapped_column(String(1), sort_order=600)
    concept_code: Mapped[str] = mapped_column(String(50), index=True, sort_order=700)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=800)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=900)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1), sort_order=1000)

    @declared_attr
    def concept_class(cls) -> Mapped["ConceptClass"]:
        return relationship("ConceptClass", foreign_keys="Concept.concept_class_id")

    @declared_attr
    def domain(cls) -> Mapped["Domain"]:
        return relationship("Domain", foreign_keys="Concept.domain_id")

    @declared_attr
    def vocabulary(cls) -> Mapped["Vocabulary"]:
        return relationship("Vocabulary", foreign_keys="Concept.vocabulary_id")


class BaseConceptAncestorCdm531:
    __tablename__ = "concept_ancestor"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    ancestor_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=100
    )
    descendant_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=200
    )
    min_levels_of_separation: Mapped[int] = mapped_column(Integer, sort_order=300)
    max_levels_of_separation: Mapped[int] = mapped_column(Integer, sort_order=400)

    @declared_attr
    def ancestor_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptAncestor.ancestor_concept_id")

    @declared_attr
    def descendant_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptAncestor.descendant_concept_id")


class BaseConceptClassCdm531:
    __tablename__ = "concept_class"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    concept_class_id: Mapped[str] = mapped_column(String(20), primary_key=True, sort_order=100)
    concept_class_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    concept_class_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)

    @declared_attr
    def concept_class_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptClass.concept_class_concept_id")


class BaseConceptRelationshipCdm531:
    __tablename__ = "concept_relationship"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    concept_id_1: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=100)
    concept_id_2: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=200)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey(f"{VOCAB_SCHEMA}.relationship.relationship_id"), primary_key=True, index=True, sort_order=300
    )
    valid_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=400)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=500)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1), sort_order=600)

    @declared_attr
    def concept_1(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptRelationship.concept_id_1")

    @declared_attr
    def concept_2(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptRelationship.concept_id_2")

    @declared_attr
    def relationship(cls) -> Mapped["Relationship"]:
        return relationship("Relationship", foreign_keys="ConceptRelationship.relationship_id")


class BaseConceptSynonymCdm531:
    __tablename__ = "concept_synonym"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=100)
    concept_synonym_name: Mapped[str] = mapped_column(String(1000), primary_key=True, sort_order=200)
    language_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), primary_key=True, sort_order=300)

    @declared_attr
    def concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptSynonym.concept_id")

    @declared_attr
    def language_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConceptSynonym.language_concept_id")


class BaseDomainCdm531:
    __tablename__ = "domain"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    domain_id: Mapped[str] = mapped_column(String(20), primary_key=True, sort_order=100)
    domain_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    domain_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)

    @declared_attr
    def domain_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Domain.domain_concept_id")


class BaseDrugStrengthCdm531:
    __tablename__ = "drug_strength"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    drug_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=100
    )
    ingredient_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=200
    )
    amount_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=300)
    amount_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    numerator_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=500)
    numerator_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    denominator_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=700)
    denominator_unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    box_size: Mapped[Optional[int]] = mapped_column(Integer, sort_order=900)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=1000)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=1100)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1), sort_order=1200)

    @declared_attr
    def amount_unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugStrength.amount_unit_concept_id")

    @declared_attr
    def denominator_unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugStrength.denominator_unit_concept_id")

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugStrength.drug_concept_id")

    @declared_attr
    def ingredient_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugStrength.ingredient_concept_id")

    @declared_attr
    def numerator_unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugStrength.numerator_unit_concept_id")


class BaseRelationshipCdm531:
    __tablename__ = "relationship"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    relationship_id: Mapped[str] = mapped_column(String(20), primary_key=True, sort_order=100)
    relationship_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    is_hierarchical: Mapped[str] = mapped_column(String(1), sort_order=300)
    defines_ancestry: Mapped[str] = mapped_column(String(1), sort_order=400)
    reverse_relationship_id: Mapped[str] = mapped_column(
        ForeignKey(f"{VOCAB_SCHEMA}.relationship.relationship_id"), sort_order=500
    )
    relationship_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)

    @declared_attr
    def relationship_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Relationship.relationship_concept_id")

    @declared_attr
    def reverse_relationship(cls) -> Mapped["Relationship"]:
        return relationship("Relationship", foreign_keys="Relationship.reverse_relationship_id")


class BaseVocabularyCdm531:
    __tablename__ = "vocabulary"
    __table_args__ = {"schema": VOCAB_SCHEMA}

    vocabulary_id: Mapped[str] = mapped_column(String(20), primary_key=True, sort_order=100)
    vocabulary_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    vocabulary_reference: Mapped[str] = mapped_column(String(255), sort_order=300)
    vocabulary_version: Mapped[Optional[str]] = mapped_column(String(255), sort_order=400)
    vocabulary_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)

    @declared_attr
    def vocabulary_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Vocabulary.vocabulary_concept_id")


class BaseSourceToConceptMapCdm531:
    __tablename__ = "source_to_concept_map"
    __table_args__ = {"schema": CDM_SCHEMA}

    source_code: Mapped[str] = mapped_column(String(1000), primary_key=True, index=True, sort_order=100)
    source_concept_id: Mapped[int] = mapped_column(Integer, sort_order=200)
    source_vocabulary_id: Mapped[str] = mapped_column(
        ForeignKey(FK_VOCABULARY_ID), primary_key=True, index=True, sort_order=300
    )
    source_code_description: Mapped[Optional[str]] = mapped_column(String(255), sort_order=400)
    target_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, index=True, sort_order=500
    )
    target_vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), index=True, sort_order=600)
    valid_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=700)
    valid_end_date: Mapped[datetime.date] = mapped_column(Date, primary_key=True, sort_order=800)
    invalid_reason: Mapped[Optional[str]] = mapped_column(String(1), sort_order=900)

    @declared_attr
    def source_vocabulary(cls) -> Mapped["Vocabulary"]:
        return relationship("Vocabulary", foreign_keys="SourceToConceptMap.source_vocabulary_id")

    @declared_attr
    def target_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SourceToConceptMap.target_concept_id")

    @declared_attr
    def target_vocabulary(cls) -> Mapped["Vocabulary"]:
        return relationship("Vocabulary", foreign_keys="SourceToConceptMap.target_vocabulary_id")


class BaseSourceToConceptMapVersionCdm531:
    __tablename__ = "source_to_concept_map_version"
    __table_args__ = {"schema": CDM_SCHEMA}

    source_vocabulary_id: Mapped[str] = mapped_column(ForeignKey(FK_VOCABULARY_ID), primary_key=True, sort_order=100)
    stcm_version: Mapped[str] = mapped_column(String(255), sort_order=200)
    last_upload_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, sort_order=300
    )

    @declared_attr
    def source_vocabulary(cls) -> Mapped["Vocabulary"]:
        return relationship("Vocabulary", foreign_keys="SourceToConceptMapVersion.source_vocabulary_id")
