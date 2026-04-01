from pathlib import Path
import subprocess

import pytest


@pytest.fixture(autouse=True)
def chdir_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    testing_folder = Path(__file__).parent / "subproject"
    monkeypatch.chdir(testing_folder)


def test_1() -> None:
    assert 5 == 5


def test_run_uv_nox() -> None:
    a = subprocess.run(["uv", "run", "python", "-m", "nox"])
    assert a.returncode == 0


def test_run_failed_uv_venv() -> None:
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", "failed_virtualenv"], capture_output=True
    )
    assert a.returncode == 1  # This test is expected to fail with a `Session.error` raised.
    assert "is not allowed" in a.stderr.decode()

    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", "failed_venv_none"], capture_output=True
    )
    assert a.returncode == 1  # This test is expected to fail with a `Session.error` raised.
    assert "is not allowed" in a.stderr.decode()
