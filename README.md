## Intro

[![GitHub Actions][github-actions-badge]](https://github.com/dantebben/nox-uv/actions)
[![uv][uv-badge]](https://github.com/astral-sh/uv)
[![Nox][nox-badge]](https://github.com/wntrblm/nox)
[![Ruff][ruff-badge]](https://github.com/astral-sh/ruff)
[![Type checked with mypy][mypy-badge]](https://mypy-lang.org/)

[github-actions-badge]: https://github.com/dantebben/nox-uv/workflows/CI/badge.svg
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[nox-badge]: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg

`nox-uv` is a basic drop-in replacement for `nox.session` of [nox](https://nox.thea.codes/) to be
used with the [uv](https://docs.astral.sh/uv/) package manager.

To use, import `session` from `nox_uv` in your `noxfile.py`.

> [!NOTE]
> All `@session(...)` parameters are keywords only, no positional parameters are allowed.

> [!NOTE]
> The `default_groups` defined in `pyproject.toml` are _not_ installed by default. The
> user must explicitly list the desired groups in the `uv_groups` parameter. 

## Added parameters

- `uv_groups`: list of `uv` dependency groups
- `uv_extras`: list of `uv` extras
- `uv_all_extras`: boolean to install all extras from `pyproject.toml`
- `uv_all_groups`: boolean to install all dependency groups

## Inspiration

This is heavily influenced by, but much more limited than, 
[nox-poetry](https://nox-poetry.readthedocs.io).
