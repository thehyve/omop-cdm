"""OMOP CDM legacy tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID

FK_COHORT_DEFINITION_ID = f"{CDM_SCHEMA}.cohort_definition.cohort_definition_id"


class BaseCohort:
    __tablename__ = "cohort"
    __table_args__ = {"schema": CDM_SCHEMA}

    cohort_definition_id: Mapped[int] = mapped_column(
        ForeignKey(FK_COHORT_DEFINITION_ID), primary_key=True, index=True, sort_order=100
    )
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, sort_order=200)
    cohort_start_date: Mapped[Date] = mapped_column(Date, primary_key=True, sort_order=300)
    cohort_end_date: Mapped[Date] = mapped_column(Date, primary_key=True, sort_order=400)

    @declared_attr
    def cohort_definition(cls) -> Mapped["CohortDefinition"]:
        return relationship("CohortDefinition")


class BaseCohortDefinition:
    __tablename__ = "cohort_definition"
    __table_args__ = {"schema": CDM_SCHEMA}

    cohort_definition_id: Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True, sort_order=100)
    cohort_definition_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    cohort_definition_description: Mapped[Optional[str]] = mapped_column(Text, sort_order=300)
    definition_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    cohort_definition_syntax: Mapped[Optional[str]] = mapped_column(Text, sort_order=500)
    subject_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    cohort_initiation_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=700)

    @declared_attr
    def definition_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="CohortDefinition.definition_type_concept_id")

    @declared_attr
    def subject_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="CohortDefinition.subject_concept_id")


class BaseCohortAttribute:
    __tablename__ = "cohort_attribute"
    __table_args__ = {"schema": CDM_SCHEMA}

    cohort_definition_id: Mapped[int] = mapped_column(
        ForeignKey(FK_COHORT_DEFINITION_ID), primary_key=True, index=True, sort_order=100
    )
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=200)
    cohort_start_date: Mapped[datetime.date] = mapped_column(Date, primary_key=True, sort_order=300)
    cohort_end_date: Mapped[datetime.date] = mapped_column(Date, primary_key=True, sort_order=400)
    attribute_definition_id: Mapped[int] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.attribute_definition.attribute_definition_id"),
        primary_key=True,
        index=True,
        sort_order=500,
    )
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=600)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)

    @declared_attr
    def cohort_definition(cls) -> Mapped["CohortDefinition"]:
        return relationship("CohortDefinition")

    @declared_attr
    def attribute_definition(cls) -> Mapped["AttributeDefinition"]:
        return relationship("AttributeDefinition")

    @declared_attr
    def value_as_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept")


class BaseAttributeDefinition:
    __tablename__ = "attribute_definition"
    __table_args__ = {"schema": CDM_SCHEMA}

    attribute_definition_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, sort_order=100)
    attribute_name: Mapped[str] = mapped_column(String(255), sort_order=200)
    attribute_description: Mapped[Optional[str]] = mapped_column(Text, sort_order=300)
    attribute_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    attribute_syntax: Mapped[Optional[str]] = mapped_column(Text, sort_order=500)

    @declared_attr
    def attribute_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept")
