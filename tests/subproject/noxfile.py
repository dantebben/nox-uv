from nox import Session, options

from nox_uv import session

options.default_venv_backend = "uv"
options.reuse_existing_virtualenvs = False

options.sessions = [
    "check_python_version",
    "install_nothing",
    "only_test_group",
    "all_groups",
    "all_extras",
    "only_one_extra",
    "correct_python",
]


@session(venv_backend="none")
def check_python_version(s: Session) -> None:
    s.run("python3", "--version")


@session
def install_nothing(s: Session) -> None:
    r = s.run("uv", "pip", "list", silent=True)
    assert isinstance(r, str)
    assert "nox-uv" in r
    assert "scapy" not in r
    assert "pyyaml" not in r
    assert "networkx" not in r
    assert "ruff" not in r
    assert "pytest-cov" not in r
    assert "mypy" not in r


@session(uv_groups=["test"])
def only_test_group(s: Session) -> None:
    r = s.run("uv", "pip", "list", silent=True)
    assert isinstance(r, str)
    assert "pytest-cov" in r
    assert "networkx" not in r
    assert "ruff" not in r


@session(uv_all_groups=True)
def all_groups(s: Session) -> None:
    r = s.run("uv", "pip", "list", silent=True)
    assert isinstance(r, str)
    assert "networkx" in r
    assert "ruff" in r
    assert "pytest-cov" in r
    assert "mypy" in r


@session(uv_all_extras=True)
def all_extras(s: Session) -> None:
    r = s.run("uv", "pip", "list", silent=True)
    assert isinstance(r, str)
    assert "networkx" not in r
    assert "scapy" in r
    assert "pyyaml" in r


@session(uv_extras=["pyyaml"])
def only_one_extra(s: Session) -> None:
    r = s.run("uv", "pip", "list", silent=True)
    assert isinstance(r, str)
    assert "networkx" not in r
    assert "pyyaml" in r


@session(python=["3.10"])
def correct_python(s: Session) -> None:
    assert s.python == "3.10"
    v = s.run("python3", "--version", silent=True)
    if isinstance(v, str):
        assert "Python 3.10" in v
    else:
        raise RuntimeError("Python version was not returned.")
