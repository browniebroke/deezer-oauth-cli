import subprocess
import sys


def test_can_run_as_python_module():
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "deezer_oauth", "--help"],
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"deezer-oauth [OPTIONS]" in result.stdout
