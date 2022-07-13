from typer.testing import CliRunner

from deezer_oauth.main import app

runner = CliRunner()


def test_no_arguments():
    result = runner.invoke(app)
    assert result.exit_code == 2
    assert "Error" in result.stdout
    assert "Missing argument 'APP_ID'." in result.stdout


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Obtain an API token from Deezer." in result.stdout
