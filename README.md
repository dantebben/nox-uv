## Intro

This is a basic drop-in replacement for `nox.session` of [nox](https://nox.thea.codes/) to be used 
with the [uv](https://docs.astral.sh/uv/) package manager.

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
```

> [!NOTE]
> All `@session(...)` parameters are keywords only, no positional parameters are allowed.

> [!NOTE]
> The `default_groups` defined in `pyproject.toml` are _not_ installed by default. The
> user must explicitly list the desired groups in the `uv_groups` parameter. 

### Added parameters

- `uv_groups`: list of `uv` dependency groups
- `uv_extras`: list of `uv` extras
- `uv_all_extras`: boolean to install all extras from `pyproject.toml`
- `uv_all_groups`: boolean to install all dependency groups

## Inspiration

This is heavily influenced by, but much more limited than, 
[nox-poetry](https://nox-poetry.readthedocs.io).
