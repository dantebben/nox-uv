from pathlib import Path
import subprocess


def test_1() -> None:
    assert 5 == 5


def test_run_uv_nox() -> None:
    folder = Path(__file__).parent
    noxfile = folder / "subnoxfile.py"
    command = ["nox", "-f", f"{noxfile}"]
    a = subprocess.run(command)
    assert a.returncode == 0
