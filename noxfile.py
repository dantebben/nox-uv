from nox import Session, options, parametrize

from nox_uv import session

options.error_on_external_run = True
options.reuse_existing_virtualenvs = True
options.default_venv_backend = "uv"
options.sessions = ["uv_lock_check", "lint", "type_check", "test"]


@session(venv_backend="none")
def uv_lock_check(s: Session) -> None:
    s.run("uv", "lock", "--check")


@session(
    reuse_venv=True,
    python=["3.10", "3.11", "3.12", "3.13"],
    uv_groups=["test"],
)
def test(s: Session) -> None:
    s.run(
        "python",
        "-m",
        "pytest",
        "--cov=nox_uv",
        "--cov-report=html",
        "--cov-report=term",
        "tests",
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


@session(uv_groups=["lint"])
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


@session(venv_backend="none")
def simple_test(s: Session) -> None:
    assert 1 == 1


@session(venv_backend="none")
def run_test_as_session(s: Session) -> None:
    """Test ability to call a nother session."""
    simple_test(s)
