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
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest")


@nox.session(python="3.12")
def lint(session):
    session.run("poetry", "install", external=True)
    session.run("ruff", "check")
