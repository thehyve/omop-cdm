import nox  # type: ignore

nox.options.sessions = [
    "tests",
    "lint",
]

python = [
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
]


@nox.session(python=python)
def tests(session: nox.Session):
    """Run test suite."""
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov=src")
    session.notify("coverage")


@nox.session
def coverage(session: nox.Session):
    """Generate pytest code coverage report."""
    session.run("coverage", "report", "--show-missing")


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
