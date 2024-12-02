# omop-cdm

omop-cdm is a Python package that contains SQLAlchemy declarative table definitions of several
versions of the [OHDSI OMOP CDM](https://ohdsi.github.io/CommonDataModel/).

## Installation

omop-cdm requires Python >= 3.9.

Install from PyPI:
```shell
pip install omop-cdm
```

## Usage

See [User documentation](docs/README.md)

## Supported databases
The omop-cdm table definitions are tested to be compatible with PostgreSQL.

Though not officially supported, omop-cdm doesn't use postgres-specific features
of SQLAlchemy, so it can likely be used for other database types as well.

## CDM versions
omop-cdm contains table defintions for the following CDM versions:
- CDM 5.4
- CDM 5.3.1
- CDM 6.0.0 ([not recommended](https://ohdsi.github.io/CommonDataModel/cdm60.html#NOTE_ABOUT_CDM_v60))

## Development

### Setup steps

- Make sure [Poetry](https://python-poetry.org/docs/#installation) is installed.
- Install the project and dependencies via `poetry install`.
- Set up the pre-commit hook scripts via `poetry run pre-commit install`.

### Nox sessions

Several developer actions (e.g. run tests, code format, lint) are available
via [nox](https://nox.thea.codes/en/stable/) sessions.
For a complete list, run:
```shell
nox --list
```
