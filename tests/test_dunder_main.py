import subprocess


def test_can_run_as_python_module():
    result = subprocess.run(
        ["python", "-m", "deezer_oauth", "--help"],  # noqa S603,S607
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"deezer-oauth [OPTIONS]" in result.stdout
