from deezer_oauth.client import OAuthDancer
from deezer_oauth.server import run_server


class TestRunServer:
    def test_run_ok(self, mocker):
        serve_forever = mocker.patch("deezer_oauth.server.HTTPServer.serve_forever")
        server_close = mocker.patch("deezer_oauth.server.HTTPServer.server_close")
        run_server(OAuthDancer("a", "b"))
        serve_forever.assert_called_once()
        server_close.assert_called_once()

    def test_interrupted(self, mocker):
        serve_forever = mocker.patch(
            "deezer_oauth.server.HTTPServer.serve_forever",
            side_effect=KeyboardInterrupt(),
        )
        server_close = mocker.patch("deezer_oauth.server.HTTPServer.server_close")
        run_server(OAuthDancer("a", "b"))
        serve_forever.assert_called_once()
        server_close.assert_called_once()
