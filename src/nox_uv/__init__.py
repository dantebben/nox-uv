from __future__ import annotations

from collections.abc import Callable, Sequence
import functools
from typing import Any, TypeVar

import nox

R = TypeVar("R")

Python = Sequence[str] | str | bool | None


def session(
    *args: Any,
    python: Python | None = None,
    reuse_venv: bool | None = None,
    name: str | None = None,
    venv_backend: Any | None = None,
    venv_params: Sequence[str] = (),
    tags: Sequence[str] | None = None,
    default: bool = True,
    requires: Sequence[str] | None = None,
    uv_groups: Sequence[str] = (),
    uv_extras: Sequence[str] = (),
    uv_all_extras: bool = False,
    uv_all_groups: bool = False,
    **kwargs: dict[str, Any],
) -> Callable[..., Callable[..., R]]:
    """Drop-in replacement for the :func:`nox.session` decorator to add support for `uv`.

    Args:
        args: Positional arguments are forwarded to ``nox.session``.
        kwargs: Keyword arguments are forwarded to ``nox.session``. Used to catch any future
            arguments of nox.session that aren't explicitely captured in nox_uv.session.

    Returns:
        The decorated session function.
    """
    if not args:
        return functools.partial(
            session,
            python=python,
            reuse_venv=reuse_venv,
            name=name,
            venv_backend=venv_backend,
            venv_params=venv_params,
            tags=tags,
            default=default,
            requires=requires,
            uv_groups=uv_groups,
            uv_extras=uv_extras,
            uv_all_extras=uv_all_extras,
            uv_all_groups=uv_all_groups,
            **kwargs,
        )  # type: ignore

    [function] = args

    if venv_backend is None:
        venv_backend = nox.options.default_venv_backend

    is_uv = venv_backend == "uv"

    # Create the `uv sync` command
    sync_cmd = ["uv", "sync", "--no-default-groups"]

    # Add the groups
    for g in uv_groups:
        sync_cmd.append(f"--group={g}")

    # Add the extras
    for e in uv_extras:
        sync_cmd.append(f"--extra={e}")

    if uv_all_groups:
        sync_cmd.append("--all-groups")

    if uv_all_extras:
        sync_cmd.append("--all-extras")

    @functools.wraps(function)
    def wrapper(s: nox.Session, *_args: Any, **_kwargs: Any) -> None:
        if is_uv:
            env: dict[str, Any] = {"UV_PROJECT_ENVIRONMENT": s.virtualenv.location}

            # UV called from Nox does not respect the Python version set in the Nox session.
            # We need to pass the Python version to UV explicitly.
            if s.python is not None:
                env["UV_PYTHON"] = s.python

            s.run_install(
                *sync_cmd,
                env=env,
            )
        function(nox.Session(s._runner), *_args, **_kwargs)

    return nox.session(  # type: ignore
        wrapper,
        python=python,
        reuse_venv=reuse_venv,
        name=name,
        venv_backend=venv_backend,
        venv_params=venv_params,
        tags=tags,
        default=default,
        requires=requires,
        **kwargs,
    )
