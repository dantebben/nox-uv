from nox import Session, options

from nox_uv import session

options.default_venv_backend = "uv"

options.sessions = [
    "nox_test_1",
    "nox_test_2",
    "nox_test_3",
    "nox_test_4",
    "nox_test_5",
]


@session(venv_backend="none")
def nox_test_1(s: Session) -> None:
    s.run("python3", "--version")


@session(uv_groups=["test"])
def nox_test_2(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "pytest-cov" in r
        assert "networkx" not in r


@session(uv_all_groups=True)
def nox_test_3(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "pytest-cov" in r
        assert "networkx" in r


@session(uv_all_extras=True)
def nox_test_5(s: Session) -> None:
    s.install("pip")
    r = s.run("python3", "-m", "pip", "list", silent=True)
    if isinstance(r, str):
        assert "networkx" not in r
        assert "plotly" in r


@session(python=["3.10"])
def nox_test_4(s: Session) -> None:
    assert s.python == "3.10"
    v = s.run("python3", "--version", silent=True)
    if isinstance(v, str):
        assert "Python 3.10" in v
    else:
        raise RuntimeError("Python version was not returned.")
