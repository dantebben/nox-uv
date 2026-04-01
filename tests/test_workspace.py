from pathlib import Path
import subprocess

import pytest


@pytest.fixture(autouse=True)
def chdir_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    testing_folder = Path(__file__).parent / "subworkspace"
    monkeypatch.chdir(testing_folder)


@pytest.mark.parametrize(
    "session_name",
    [
        "run_package_one_with_its_package",
        "run_package_two_with_its_package",
        "run_both_packages_with_both_explicitly_listed",
        "run_both_packages_with_all_packages",
    ],
)
def test_expected_success(session_name: str) -> None:
    a = subprocess.run(["uv", "run", "python", "-m", "nox", "-s", session_name])
    assert a.returncode == 0


@pytest.mark.parametrize(
    ("session_name", "expect_in_error"),
    [
        ("run_package_one_with_no_packages", "package-one-bin not found."),
        ("run_package_two_with_no_packages", "package-two-bin not found."),
        ("run_package_one_with_package_two", "package-one-bin not found."),
        ("run_package_two_with_package_one", "package-two-bin not found."),
        (
            "run_explicit_and_all_packages",
            "uv_packages and uv_all_packages are mututally exclusive",
        ),
    ],
)
def test_expected_failure(session_name: str, expect_in_error: str) -> None:
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", session_name], capture_output=True, text=True
    )
    assert a.returncode == 1
    assert expect_in_error in a.stderr
