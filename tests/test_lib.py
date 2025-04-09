from pathlib import Path
import subprocess


def test_1() -> None:
    assert 5 == 5


def test_run_uv_nox() -> None:
    folder = Path(__file__).parent
    noxfile = folder / "subnoxfile.py"
    a = subprocess.run(["python3", "-m", "nox", "-f", f"{noxfile}"])
    assert a.returncode == 0
