from nox import Session, options

from nox_uv import session

options.default_venv_backend = "uv"

PKG_ONE = "package-one"
PKG_TWO = "package-two"


def _run_binaries(s: Session) -> None:
    for run_binary in s.posargs:
        s.run(run_binary)


@session
def run_with_no_packages(s: Session) -> None:
    _run_binaries(s)


@session(uv_packages=[PKG_ONE])
def run_with_package_one(s: Session) -> None:
    _run_binaries(s)


@session(uv_packages=[PKG_TWO])
def run_with_package_two(s: Session) -> None:
    _run_binaries(s)


@session(uv_packages=[PKG_ONE, PKG_TWO])
def run_with_packages_one_and_two(s: Session) -> None:
    _run_binaries(s)


@session(uv_all_packages=True)
def run_with_all_packages(s: Session) -> None:
    _run_binaries(s)


@session(uv_packages=[PKG_ONE], uv_all_packages=True)
def run_explicit_and_all_packages(s: Session) -> None:
    _run_binaries(s)
