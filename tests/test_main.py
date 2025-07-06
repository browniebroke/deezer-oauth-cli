from typer.testing import CliRunner

from deezer_oauth.main import app

runner = CliRunner()


def test_no_arguments():
    result = runner.invoke(app)
    assert result.exit_code == 2
    assert "Error" in result.stderr
    assert "Missing argument 'APP_ID'." in result.stderr


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Get an API token from Deezer." in result.stdout


def test_main_flow(mocker):
    """Test the main OAuth flow execution."""
    mock_dancer = mocker.MagicMock()
    mock_dancer.get_auth_page.return_value = "https://example.com/oauth"

    mock_oauth_dancer = mocker.patch(
        "deezer_oauth.main.OAuthDancer", return_value=mock_dancer
    )
    mock_webbrowser = mocker.patch("deezer_oauth.main.webbrowser.open")
    mock_run_server = mocker.patch("deezer_oauth.main.run_server")

    result = runner.invoke(app, ["test-id", "test-secret"])

    assert result.exit_code == 0
    assert "Opening https://example.com/oauth in web browser..." in result.stdout

    mock_oauth_dancer.assert_called_once_with(
        app_id="test-id",
        app_secret="test-secret",  # noqa: S106
    )
    mock_webbrowser.assert_called_once_with("https://example.com/oauth")
    mock_run_server.assert_called_once_with(mock_dancer)
