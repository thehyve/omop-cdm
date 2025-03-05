# omop-cdm

[![tests](https://github.com/thehyve/omop-cdm/actions/workflows/python-package.yml/badge.svg)](https://github.com/thehyve/omop-cdm/actions/workflows/python-package.yml)
[![PyPI Latest Release](https://img.shields.io/pypi/v/omop-cdm.svg)](https://pypi.org/project/omop-cdm/)
[![License](https://img.shields.io/pypi/l/omop-cdm.svg)](https://github.com/thehyve/omop-cdm/blob/main/LICENSE)

omop-cdm is a Python package that contains SQLAlchemy declarative table definitions of several
versions of the [OHDSI OMOP CDM](https://ohdsi.github.io/CommonDataModel/).

## Installation

omop-cdm requires Python >= 3.9.

Install from PyPI:
```shell
pip install omop-cdm
```

## Usage

See [User documentation](https://github.com/thehyve/omop-cdm/blob/main/docs/README.md)

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

### Releasing

omop-cdm uses [semantic versioning](https://semver.org/).

Releases should be made from the main branch. Before creating a release on
GitHub, make sure the CHANGELOG has been updated and the version number in
pyproject.toml is correct.

Once the GitHub release has been made, the package will be automatically uploaded
to PyPI (via the publish.yml workflow).
