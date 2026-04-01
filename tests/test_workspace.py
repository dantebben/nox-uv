from pathlib import Path
import subprocess

import pytest

PKG_ONE_BIN = "package-one-bin"
PKG_TWO_BIN = "package-two-bin"
PKG_ONE_GREETING = "Hello from package-one!"
PKG_TWO_GREETING = "Hello from package-two!"


@pytest.fixture(autouse=True)
def chdir_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    testing_folder = Path(__file__).parent / "subworkspace"
    monkeypatch.chdir(testing_folder)


@pytest.mark.parametrize(
    ("session_name", "run_binary", "expect_in_stdout"),
    [
        ("run_with_package_one", PKG_ONE_BIN, PKG_ONE_GREETING),
        ("run_with_package_two", PKG_TWO_BIN, PKG_TWO_GREETING),
        ("run_with_packages_one_and_two", PKG_ONE_BIN, PKG_ONE_GREETING),
        ("run_with_packages_one_and_two", PKG_TWO_BIN, PKG_TWO_GREETING),
        ("run_with_all_packages", PKG_ONE_BIN, PKG_ONE_GREETING),
        ("run_with_all_packages", PKG_TWO_BIN, PKG_TWO_GREETING),
    ],
)
def test_expected_success(
    session_name: str,
    run_binary: str,
    expect_in_stdout: str,
) -> None:
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", session_name, "--", run_binary],
        capture_output=True,
        text=True,
    )
    assert a.returncode == 0, a.stderr
    assert expect_in_stdout in a.stdout


@pytest.mark.parametrize(
    ("session_name", "run_binary", "expect_in_stderr"),
    [
        ("run_with_no_packages", PKG_ONE_BIN, "package-one-bin not found."),
        ("run_with_no_packages", PKG_TWO_BIN, "package-two-bin not found."),
        ("run_with_package_one", PKG_TWO_BIN, "package-two-bin not found."),
        ("run_with_package_two", PKG_ONE_BIN, "package-one-bin not found."),
        (
            "run_explicit_and_all_packages",
            PKG_ONE_BIN,
            "uv_packages and uv_all_packages are mututally exclusive",
        ),
    ],
)
def test_expected_failure(
    session_name: str,
    run_binary: str,
    expect_in_stderr: str,
) -> None:
    a = subprocess.run(
        ["uv", "run", "python", "-m", "nox", "-s", session_name, "--", run_binary],
        capture_output=True,
        text=True,
    )
    assert a.returncode == 1
    assert expect_in_stderr in a.stderr
