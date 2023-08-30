import http.client
import sys
import threading

if sys.version_info < (3, 10):
    from test.support import threading_cleanup, threading_setup
else:
    from test.support.threading_helper import threading_cleanup, threading_setup

import pytest

from deezer_oauth.client import OAuthDancer
from deezer_oauth.server import LocalHTTPServer, LocalRequestHandler, run_server


class TestRunServer:
    def test_run_ok(self, mocker):
        serve_forever = mocker.patch("deezer_oauth.server.HTTPServer.serve_forever")
        server_close = mocker.patch("deezer_oauth.server.HTTPServer.server_close")
        run_server(OAuthDancer("a", "b"))
        serve_forever.assert_called_once()
        server_close.assert_called_once()

    @pytest.mark.parametrize("exception_class", [KeyboardInterrupt, SystemExit])
    def test_interrupted(self, mocker, exception_class):
        mocker.patch("deezer_oauth.server.HTTPServer.__init__")
        serve_forever = mocker.patch(
            "deezer_oauth.server.HTTPServer.serve_forever",
            side_effect=exception_class(),
        )
        server_close = mocker.patch("deezer_oauth.server.HTTPServer.server_close")
        run_server(OAuthDancer("a", "b"))
        serve_forever.assert_called_once()
        server_close.assert_called_once()


class ServerWrapperThread(threading.Thread):
    """
    Run a server in a separate thread.

    Forked from a similar class from the stdlib that can be found at:
    test.test_httpservers#TestServerThread
    """

    server: LocalHTTPServer

    def __init__(self, test_class):
        threading.Thread.__init__(self)
        self.test_class = test_class

    def run(self):
        self.server = LocalHTTPServer(
            OAuthDancer("a", "b"),
            ("localhost", 0),
            LocalRequestHandler,
        )
        self.test_class.host, self.test_class.port = self.server.socket.getsockname()
        self.test_class.server_started.set()
        self.test_class = None
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()

    def stop(self):
        self.server.shutdown()
        self.join()


class TestLocalRequestHandler:
    host: str
    port: int
    server_started: threading.Event

    @pytest.fixture
    def http_server(self):
        _threads = threading_setup()
        self.server_started = threading.Event()
        thread = ServerWrapperThread(self)
        thread.start()
        self.server_started.wait()
        yield
        thread.stop()
        # clear assignment to avoid dangling thread
        thread = None  # type: ignore[assignment]
        threading_cleanup(*_threads)

    def request(self, uri, method="GET"):
        self.connection = http.client.HTTPConnection(self.host, self.port)
        self.connection.request(method, uri)
        return self.connection.getresponse()

    def test_default_route(self, http_server):
        response = self.request("/")
        assert isinstance(response, http.client.HTTPResponse)
        assert response.status == 200
        body = response.read().decode()
        assert "<title>Deezer API OAuth dancer</title>" in body
        assert "Start Oauth Flow" in body

    def test_return_route_no_query_string(self, http_server):
        response = self.request("/oauth/return")
        assert isinstance(response, http.client.HTTPResponse)
        assert response.status == 400
        body = response.read().decode()
        assert "Invalid request: missing query parameters" in body

    def test_return_route_with_query_string(self, http_server, mocker):
        mocker.patch(
            "deezer_oauth.client.OAuthDancer.get_token",
            return_value={"access_token": "something", "expires": 12345},
        )
        write_env_file = mocker.patch("deezer_oauth.server.write_env_file")
        response = self.request("/oauth/return?code=abcdef")
        assert isinstance(response, http.client.HTTPResponse)
        assert response.status == 200
        body = response.read().decode()
        assert "Token: something" in body
        assert "Expires: 12345" in body
        write_env_file.assert_called()
