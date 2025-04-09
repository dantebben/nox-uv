## Intro

This is heavliy influcenced by, but much more limited than, 
[nox-poetry](https://nox-poetry.readthedocs.io).

This is a basic drop-in replacement for `nox.session` of [nox](https://nox.thea.codes/) to be used 
with the [uv](https://docs.astral.sh/uv/) package manager.

To use, import `session` from `nox-uv` in your `nox-file`.

**NOTE**: All `@session(...)` parameters are keywords only, no positional parameters are allowed.

**NOTE**: The `default_groups` defined in `pyproject.toml` are _not_ installed by default. The
user must explicitly list the desired groups in the `uv_groups` parameter. 

## Added parameters

- `uv_groups`: list of `uv` dependency groups
- `uv_extras`: list of `uv` extras
- `uv_all_extras`: boolean to install all extras from `pyproject.toml`
- `uv_all_groups`: boolean to install all dependency groups

