from nox import Session, options, parametrize

from nox_uv import session

options.error_on_external_run = True
options.default_venv_backend = "uv"
options.sessions = ["lint", "type_check", "test"]


@session(
    python=["3.9", "3.10", "3.11", "3.12", "3.13"],
    uv_groups=["test"],
)
def test(s: Session) -> None:
    s.run(
        "python",
        "-m",
        "pytest",
        "--cov=nox_uv",
        "--cov-branch",
        "--cov-report=html",
        "--cov-report=term",
        "--cov-fail-under=100",
        "tests",
        *s.posargs,
    )


@session(uv_only_groups=["lint"])
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


@session(uv_only_groups=["lint"])
@parametrize(
    "command",
    [
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
    ],
)
def lint(s: Session, command: list[str]) -> None:
    s.run(*command)


@session(uv_only_groups=["lint"])
def lint_fix(s: Session) -> None:
    s.run("ruff", "check", ".", "--extend-fixable", "F401", "--fix")


@session(uv_groups=["test", "type_check"])
def type_check(s: Session) -> None:
    s.run("mypy", "src", "tests", "noxfile.py")
