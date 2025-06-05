from __future__ import annotations

from collections.abc import Callable, Sequence
import functools
from typing import Any, TypeVar, Union

import nox

R = TypeVar("R")

Python = Union[Sequence[str], str, bool]


def session(
    *args: Any,
    python: Python | None = None,
    reuse_venv: bool | None = None,
    name: str | None = None,
    venv_backend: str | None = None,
    venv_params: Sequence[str] = (),
    tags: Sequence[str] | None = None,
    default: bool = True,
    requires: Sequence[str] | None = None,
    uv_groups: Sequence[str] = (),
    uv_extras: Sequence[str] = (),
    uv_only_groups: Sequence[str] = (),
    uv_all_extras: bool = False,
    uv_all_groups: bool = False,
    uv_sync_locked: bool = True,
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
            uv_only_groups=uv_only_groups,
            uv_sync_locked=uv_sync_locked,
            **kwargs,
        )  # type: ignore

    [function] = args

    # Create the `uv sync` command
    sync_cmd = ["uv", "sync", "--no-default-groups"]
    extended_cmd: list[str] = []

    # Add the --locked flag
    if uv_sync_locked:
        sync_cmd.append("--locked")

    # Add the groups
    extended_cmd.extend([f"--group={g}" for g in uv_groups])

    # Add the extras
    extended_cmd.extend([f"--extra={e}" for e in uv_extras])

    # Add the only-groups
    extended_cmd.extend([f"--only-group={g}" for g in uv_only_groups])

    if uv_all_groups:
        extended_cmd.append("--all-groups")

    if uv_all_extras:
        extended_cmd.append("--all-extras")

    sync_cmd += extended_cmd

    @functools.wraps(function)
    def wrapper(s: nox.Session, *_args: Any, **_kwargs: Any) -> None:
        if s.venv_backend == "uv":
            s.env["UV_PROJECT_ENVIRONMENT"] = s.virtualenv.location

            # UV called from Nox does not respect the Python version set in the Nox session.
            # We need to pass the Python version to UV explicitly.
            if s.python is not None:
                # NOTE: casting to string explicitly because implicit casting isn't working
                # for the type checker.
                s.env["UV_PYTHON"] = str(s.python)

            s.run_install(*sync_cmd)
        else:
            if len(extended_cmd) > 0:
                raise s.error(
                    'Using "uv" specific paramaters is not allowed outside of a "uv" '
                    "venv_backend.\n"
                    f"Check the venv_backend, or the {extended_cmd} parameters."
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
