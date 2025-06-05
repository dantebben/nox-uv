## Intro

[![GitHub Actions][github-actions-badge]](https://github.com/dantebben/nox-uv/actions)
[![PyPI version][pypi-version-badge]](https://pypi.python.org/pypi/nox-uv)
[![Python versions][python-versions-badge]](https://pypi.python.org/pypi/nox-uv)
[![uv][uv-badge]](https://github.com/astral-sh/uv)
[![Nox][nox-badge]](https://github.com/wntrblm/nox)
[![Ruff][ruff-badge]](https://github.com/astral-sh/ruff)
[![Type checked with mypy][mypy-badge]](https://mypy-lang.org/)

[github-actions-badge]: https://github.com/dantebben/nox-uv/workflows/CI/badge.svg
[pypi-version-badge]: https://img.shields.io/pypi/v/nox-uv.svg
[python-versions-badge]: https://img.shields.io/pypi/pyversions/nox-uv.svg
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[nox-badge]: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg

`nox-uv` is a simple drop-in replacement for [nox](https://nox.thea.codes/)'s `@nox.session` that installs
dependencies constrained by [uv](https://docs.astral.sh/uv/)'s lockfile.

## Usage

Add `nox-uv` as a development dependency. The following example adds it into a `nox`
`dependency-group`.

```shell
uv add --group nox nox-uv
```

Using the following configuration within `pyproject.toml` as an example:

```toml
[dependency-groups]
nox = [
    "nox-uv",
]
test = [
    "pytest",
    "pytest-cov",
]
type_check = [
    "mypy",
]
lint = [
    "ruff",
]
```

Within, your `noxfile.py`:

1. Import `session` from `nox_uv`.
2. Set `venv_backend` to `"uv"`. This can be done globally using
   `options.default_venv_backend = "uv"`.
3. Use the new [`uv_*` parameters](#added-parameters) to `session` to control which dependencies
   are synced into the session's virtual environment in addition to the project's main
   dependencies.
     - `uv sync` is used to install dependencies so that their versions are constrained by
       `uv.lock`.

```py
from nox import Session, options
from nox_uv import session

options.default_venv_backend = "uv"


@session(
    python=["3.10", "3.11", "3.12", "3.13"],
    uv_groups=["test"],
)
def test(s: Session) -> None:
    s.run("python", "-m", "pytest")


@session(uv_groups=["type_check"])
def type_check(s: Session) -> None:
    s.run("mypy", "src")


@session(uv_only_groups=["lint"])
def type_check(s: Session) -> None:
    s.run("ruff", "check", ".")
    s.run("ruff", "format", "--check", ".")
```

> [!NOTE]
> All `@session(...)` parameters are keywords only, no positional parameters are allowed.

> [!NOTE]
> The `default_groups` defined in `pyproject.toml` are _not_ installed by default. The
> user must explicitly list the desired groups in the `uv_groups` parameter. 

### Added parameters

- `uv_groups`: list of `uv` _dependency-groups_
- `uv_extras`: list of `uv` _optional-dependencies_
- `uv_only_groups`: list of `uv` _only-groups_ to include. Prevents installation of project
   _dependencies_.
- `uv_all_extras`: boolean to install all _optional-dependencies_ from `pyproject.toml`
- `uv_all_groups`: boolean to install all _dependency-groups_
- `uv_sync_locked`: boolean to validate that `uv.lock` is up-to-date


## Inspiration

This is heavily influenced by, but much more limited than, 
[nox-poetry](https://nox-poetry.readthedocs.io).
