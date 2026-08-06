# Development

## Setup steps

- Make sure [Poetry](https://python-poetry.org/docs/#installation) is installed.
- Install the project and dependencies via `poetry install`.
- Set up the pre-commit hook scripts via `poetry run pre-commit install`.

## Nox sessions

Several developer actions (e.g. run tests, code format, lint) are available
via [nox](https://nox.thea.codes/en/stable/) sessions.
For a complete list, run:
```shell
nox --list
```

## Releasing

omop-cdm uses [semantic versioning](https://semver.org/).

New releases are made from the main branch. Whenever making a new release,
check the following:
- CHANGELOG.md includes a summary of all changes since the last release.
- The package version stated in pyproject.toml reflects the release you want
  to make.

Once the GitHub release has been made, the package will be automatically uploaded
to PyPI (via the publish.yml workflow).
