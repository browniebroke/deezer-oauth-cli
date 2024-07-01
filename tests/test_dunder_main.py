import subprocess
import sys


def test_can_run_as_python_module():
    result = subprocess.run(
        [sys.executable, "-m", "deezer_oauth", "--help"],  # noqa: S603
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"deezer-oauth [OPTIONS]" in result.stdout
