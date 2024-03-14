"""
OMOP CDM Version 5.4.

Generated from OMOP CDM release 5.4 using sqlacodegen 3.0.0rc5.
DDL from https://github.com/OHDSI/CommonDataModel/tree/v5.4



Deviations from standard model

Removed

cohort
cohort_attribute


Added

stem_table
source_to_concept_map_version


Updated

source_to_concept_map
    source_code from VARCHAR(50) --> VARCHAR(1000)
    If using a separate vocab schema, STCM is created in the CDM schema

"""
