from nox import Session, options

from nox_uv import session

options.default_venv_backend = "uv"

PKG_ONE = "package-one"
PKG_TWO = "package-two"
PKG_ONE_BIN = "package-one-bin"
PKG_TWO_BIN = "package-two-bin"


@session(uv_packages=[PKG_ONE])
def run_package_one_with_its_package(s: Session) -> None:
    s.run(PKG_ONE_BIN)


@session(uv_packages=[PKG_TWO])
def run_package_two_with_its_package(s: Session) -> None:
    s.run(PKG_TWO_BIN)


@session(uv_packages=[PKG_ONE, PKG_TWO])
def run_both_packages_with_both_explicitly_listed(s: Session) -> None:
    s.run(PKG_ONE_BIN)
    s.run(PKG_TWO_BIN)


@session(uv_all_packages=True)
def run_both_packages_with_all_packages(s: Session) -> None:
    s.run(PKG_ONE_BIN)
    s.run(PKG_TWO_BIN)


@session
def run_package_one_with_no_packages(s: Session) -> None:
    s.run(PKG_ONE_BIN)


@session
def run_package_two_with_no_packages(s: Session) -> None:
    s.run(PKG_TWO_BIN)


@session(uv_packages=[PKG_TWO])
def run_package_one_with_package_two(s: Session) -> None:
    s.run(PKG_ONE_BIN)


@session(uv_packages=[PKG_ONE])
def run_package_two_with_package_one(s: Session) -> None:
    s.run(PKG_TWO_BIN)


@session(uv_packages=[PKG_ONE], uv_all_packages=True)
def run_explicit_and_all_packages(s: Session) -> None:
    s.run(PKG_TWO_BIN)
