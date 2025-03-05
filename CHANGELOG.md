# Changelog

## v0.4.0

Internal changes:
- The stem_table.domain_id field has been made non-nullable for CDM 5.3, 5.4, and 6.0.

## v0.3.2

Added `__repr__` methods to all CDM 5.4 table classes.

## v0.3.1

Internal changes:
- Upgraded to Poetry 2.
- Upgraded dev and test dependencies.
- Updated metadata in pyproject.toml file.
- Use Python >= 3.9 type hints.
- Added __version__ variable

## v0.3.0

New (for CDM 5.4 onwards):
- Added cascading FKs with relationship to the person table (for easier deletion of all data related to a person).
- Made all relationships to person bidirectional for more convenient querying/analysis.

Bugfixes
- Incorrect references for payer_plan_period_id fields in CDM 5.4 ([#12](https://github.com/thehyve/omop-cdm/issues/12))
- The stem table field `start_datetime` is now nullable in CDM 5.3 and 5.4 ([#14](https://github.com/thehyve/omop-cdm/issues/14))

## v0.2.0
Update supported Python version to 3.9-3.13.

## v0.1.1
Add PyPI publish action.

## v0.1.0
First release.
