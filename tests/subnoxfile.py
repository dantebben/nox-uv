from nox import Session, options

from nox_uv import session

options.default_venv_backend = "uv"
options.reuse_venv = "yes"

options.sessions = [
    "no_backend",
    "install_single_group",
    "install_all_groups",
    "install_all_extras",
    "use_correct_python",
]


@session(venv_backend="none")
def no_backend(s: Session) -> None:
    s.run("python3", "--version")


@session(uv_groups=["test"])
def install_single_group(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "pytest-cov" in r
        assert "networkx" not in r
    else:
        raise AssertionError("pip did not return a valid list of packages")


@session(uv_all_groups=True)
def install_all_groups(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "pytest-cov" in r
        assert "networkx" in r
    else:
        raise AssertionError("pip did not return a valid list of packages")


@session(uv_all_extras=True)
def install_all_extras(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "networkx" not in r
        assert "plotly" in r
    else:
        raise AssertionError("pip did not return a valid list of packages")


@session(python=["3.10"])
def use_correct_python(s: Session) -> None:
    assert s.python == "3.10"
    v = s.run("python3", "--version", silent=True)
    if isinstance(v, str):
        assert "Python 3.10" in v
    else:
        raise RuntimeError("Python version was not returned.")
