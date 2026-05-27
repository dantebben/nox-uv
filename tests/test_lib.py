from pathlib import Path
import subprocess

TESTING_FOLDER = Path(__file__).parent / "subproject"


def test_1() -> None:
    assert 5 == 5


def test_run_uv_nox() -> None:
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox"],
        cwd=TESTING_FOLDER,
    )
    assert a.returncode == 0


def test_venv_backend_uv_no_errors() -> None:
    """Using the 'uv' backend with uv-specific parameters succeeds without errors."""
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", "test_group"],
        capture_output=True,
        cwd=TESTING_FOLDER,
    )
    assert a.returncode == 0
    assert "error" not in a.stderr.decode().lower()


def test_venv_backend_none_warning() -> None:
    """Using 'none' backend with uv-specific parameters emits a warning but succeeds."""
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", "failed_venv_none"],
        capture_output=True,
        cwd=TESTING_FOLDER,
    )
    assert a.returncode == 0
    stderr = a.stderr.decode()
    assert "No venv_backend specified, reusing existing venv." in stderr
    assert '"uv" specific parameters will be ignored.' in stderr


def test_venv_backend_other_error() -> None:
    """Using a backend other than 'uv' or 'none' with uv-specific parameters raises an error."""
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", "failed_virtualenv"],
        capture_output=True,
        cwd=TESTING_FOLDER,
    )
    assert a.returncode == 1  # This test is expected to fail with a `Session.error` raised.
    assert "is not allowed" in a.stderr.decode()
