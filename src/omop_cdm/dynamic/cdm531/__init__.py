"""
OMOP CDM Version 5.3.1.

Generated from OMOP CDM release 5.3.1 using sqlacodegen 3.0.0rc5.
DDL from https://github.com/OHDSI/CommonDataModel/tree/v5.3.1.



Deviations from standard model

Removed

attribute_definition
cohort_attribute


Added

stem_table
source_to_concept_map_version


Updated

source_to_concept_map
    source_code from VARCHAR(50) --> VARCHAR(1000)
    If using a separate vocab schema, STCM is created in the CDM schema

"""
