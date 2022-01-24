from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qsl

from deezer_oauth.constants import HOST_NAME, OAUTH_RETURN_PATH, SERVER_PORT
from deezer_oauth.files import write_env_file

if TYPE_CHECKING:
    from deezer_oauth.client import OAuthDancer


def run_server(oauth_dancer: OAuthDancer) -> None:
    """Start local webserver."""
    webserver = LocalHTTPServer(
        oauth_dancer,
        (HOST_NAME, SERVER_PORT),
        LocalRequestHandler,
    )

    # Wait for user action and display token when finished
    try:
        webserver.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        webserver.server_close()


class LocalHTTPServer(HTTPServer):
    """An HTTP Server that keeps a reference to the OAuth dancer."""

    oauth_dancer: OAuthDancer

    def __init__(self, dancer: OAuthDancer, *args: Any, **kwargs: Any) -> None:
        self.oauth_dancer = dancer
        super().__init__(*args, **kwargs)


PAGE_CONTENT = """
<html>
<head><title>Deezer API OAuth dancer</title></head>
<body>
<p>
    {content}
</p>
</body>
</html>
"""


class LocalRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler to perform the OAuth dance."""

    server: LocalHTTPServer

    @property
    def oauth_dancer(self) -> OAuthDancer:
        """Shortcut to access the `OAuthDancer` instance."""
        return self.server.oauth_dancer

    def do_GET(self) -> None:
        """Route GET requests to the right handler."""
        if self.path.startswith(OAUTH_RETURN_PATH):
            self.return_route()
        else:
            self.default_route()

    def return_route(self) -> None:
        """
        Handle the route for the OAuth return page.

        Once the OAuth is approved, Deezer redirects to this route with `?code=blah`
        at the end of the URL.

        Grab this code, make the API call to obtain the token and display it.
        """
        path_bits = self.path.split("?", 1)
        if len(path_bits) < 2:
            self._render_content(
                "Invalid request: missing query parameters",
                status=400,
            )
            return
        query_params = dict(parse_qsl(path_bits[1]))
        token_data = self.oauth_dancer.get_token(query_params["code"])
        content = (
            f"Token: {token_data['access_token']}"
            "<br>"
            f"Expires: {token_data['expires']}"
        )
        self._render_content(content)
        write_env_file(token_data["access_token"])
        raise SystemExit("All Done")

    def default_route(self) -> None:
        """Default route rendering a generic page."""
        start_url = self.oauth_dancer.get_auth_page()
        self._render_content(f'<a href="{start_url}">Start Oauth Flow</a>')

    def _render_content(self, content: str, status: int = 200) -> None:
        """Render the provided content in an HTML page."""
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_str = PAGE_CONTENT.format(content=content)
        self.wfile.write(content_str.encode())
