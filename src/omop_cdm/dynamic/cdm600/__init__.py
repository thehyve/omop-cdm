"""
OMOP CDM Version 6.0.0.

Generated with python using sqlacodegen 3.0.0rc5, model from
https://github.com/OHDSI/CommonDataModel/tree/Dev/PostgreSQL,
commit 30d851a.



Deviations from standard model

Added

stem_table
source_to_concept_map_version


Updated

source_to_concept_map
    source_code from VARCHAR(50) --> VARCHAR(1000)
    If using a separate vocab schema, STCM is created in the CDM schema

"""
