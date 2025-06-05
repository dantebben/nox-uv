import os
from pathlib import Path
import subprocess


def test_1() -> None:
    assert 5 == 5


def test_run_uv_nox() -> None:
    cur_folder = Path.cwd()
    testing_folder = Path(__file__).parent / "subproject"
    os.chdir(testing_folder)
    a = subprocess.run(["uv", "run", "python", "-m", "nox"])
    assert a.returncode == 0
    os.chdir(cur_folder)


def test_run_failed_uv_venv() -> None:
    cur_folder = Path.cwd()
    testing_folder = Path(__file__).parent / "subproject"
    os.chdir(testing_folder)
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

    os.chdir(cur_folder)
