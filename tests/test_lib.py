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
