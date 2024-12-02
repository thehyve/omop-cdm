import nox  # type: ignore

nox.options.sessions = [
    "tests",
    "lint",
]

python = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
]


@nox.session(python=python)
def tests(session: nox.Session):
    """Run pytest + code coverage."""
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov-report", "term-missing", "--cov=src")


@nox.session(reuse_venv=True, name="format")
def format_all(session: nox.Session):
    """Format codebase with ruff."""
    session.run("poetry", "install", "--only", "dev", external=True)
    session.run("ruff", "format")
    # format imports according to isort via ruff check
    session.run("ruff", "check", "--select", "I", "--fix")


@nox.session(reuse_venv=True)
def lint(session: nox.Session):
    """Run ruff linter."""
    session.run("poetry", "install", "--only", "dev", external=True)
    # Run the ruff linter
    session.run("ruff", "check")
    # Check if any code requires formatting via ruff format
    session.run("ruff", "format", "--diff")
