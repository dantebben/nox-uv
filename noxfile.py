from nox import Session, options, parametrize

from nox_uv import session

options.error_on_external_run = True
options.reuse_existing_virtualenvs = True
options.sessions = ["lint", "type_check", "test"]


# Including Python 3.9 here just to test when UV_PYTHON_DOWNLOADS=never
@session(
    venv_backend="uv",
    reuse_venv=True,
    python=["3.9", "3.10", "3.11", "3.12", "3.13"],
    uv_groups=["test"],
    uv_all_groups=True,
)
def test(s: Session) -> None:
    s.run(
        "pytest",
        *s.posargs,
    )


# For some sessions, set venv_backend="none" to simply execute scripts within the existing Poetry
# environment. This requires that nox is run within `poetry shell` or using `poetry run nox ...`.
@session(venv_backend="none")
@parametrize(
    "command",
    [
        # During formatting, additionally sort imports and remove unused imports.
        [
            "ruff",
            "check",
            ".",
            "--select",
            "I",
            "--select",
            "F401",
            "--extend-fixable",
            "F401",
            "--fix",
        ],
        ["ruff", "format", "."],
    ],
)
def fmt(s: Session, command: list[str]) -> None:
    s.run(*command)


@session(venv_backend="uv", uv_groups=["lint"])
@parametrize(
    "command",
    [
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
    ],
)
def lint(s: Session, command: list[str]) -> None:
    s.run(*command)


@session(venv_backend="none")
def lint_fix(s: Session) -> None:
    s.run("ruff", "check", ".", "--extend-fixable", "F401", "--fix")


@session(venv_backend="none")
def type_check(s: Session) -> None:
    s.run("mypy", "src", "tests", "noxfile.py")
