"""Module containing the placeholder schema names as used in the ORM."""

# These are the placeholder schema names as used in the ORM table
# definitions. They will be replaced with actual schema names at runtime
# by providing a schema_translate_map to your SQLAlchemy engine.
VOCAB_SCHEMA = "vocabulary_schema"
CDM_SCHEMA = "cdm_schema"

# Some often used foreign keys are added as variables for convenience.
FK_CONCEPT_ID = f"{VOCAB_SCHEMA}.concept.concept_id"
FK_VOCABULARY_ID = f"{VOCAB_SCHEMA}.vocabulary.vocabulary_id"
FK_DOMAIN_ID = f"{VOCAB_SCHEMA}.domain.domain_id"
FK_CONCEPT_CLASS_ID = f"{VOCAB_SCHEMA}.concept_class.concept_class_id"
FK_PERSON_ID = f"{CDM_SCHEMA}.person.person_id"
FK_VISIT_OCCURRENCE_ID = f"{CDM_SCHEMA}.visit_occurrence.visit_occurrence_id"
FK_VISIT_DETAIL_ID = f"{CDM_SCHEMA}.visit_detail.visit_detail_id"
FK_PROVIDER_ID = f"{CDM_SCHEMA}.provider.provider_id"
FK_CARE_SITE_ID = f"{CDM_SCHEMA}.care_site.care_site_id"
FK_LOCATION_ID = f"{CDM_SCHEMA}.location.location_id"

# This object should be used to set the naming_convention parameter of
# the SQLAlchemy MetaData object. Using it makes sure that the naming of
# constraints and indexes is deterministic and not left up to the DBMS.
# It's also needed when dropping these, as SQLAlchemy requires that
# they have a name for them to be dropped. See:
# https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-constraint-naming-conventions
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
