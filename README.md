# omop-cdm

[![tests](https://github.com/thehyve/omop-cdm/actions/workflows/python-package.yml/badge.svg)](https://github.com/thehyve/omop-cdm/actions/workflows/python-package.yml)
[![PyPI Latest Release](https://img.shields.io/pypi/v/omop-cdm.svg)](https://pypi.org/project/omop-cdm/)
[![License](https://img.shields.io/pypi/l/omop-cdm.svg)](https://github.com/thehyve/omop-cdm/blob/main/LICENSE)

omop-cdm is a Python package that contains SQLAlchemy declarative table definitions of several
versions of the [OHDSI OMOP CDM](https://ohdsi.github.io/CommonDataModel/).

It can be used for both data mapping and data analysis/exploration workflows.

## Installation

omop-cdm requires Python >= 3.10.

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

## Getting Involved
- Any bugs, issues or ideas for improvement can be submitted via the
  GitHub [Issues](https://github.com/thehyve/omop-cdm/issues) page.
- If you are developing on the project, please see the [contributing](CONTRIBUTING.md) guide.
