"""Simple script to obtain an API token via OAuth."""
from __future__ import annotations

import re
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlencode

import requests
import typer
from jinja2 import Template

REDIRECT_PATH = "/oauth/return"
WRITE_ENV_HELP = (
    "Whether the API token should be written to a .env file in the current directory."
)
ENV_VAR_NAME_HELP = (
    "The name of the environment variable to use when writing to the .env file."
)

app = typer.Typer()


@app.command()
def main(
    app_id: str = typer.Argument(..., help="Deezer Application ID"),
    app_secret: str = typer.Argument(..., help="Secret Key of the application"),
    hostname: str = typer.Option("localhost", help="For the redirect URL."),
    port: int = typer.Option(8080, help="For the redirect URL."),
    write_env: bool = typer.Option(True, help=WRITE_ENV_HELP),
    env_var_name: str = typer.Option("API_TOKEN", help=ENV_VAR_NAME_HELP),
):
    """
    Obtain an API token from Deezer.

    You should log in/signup at https://developers.deezer.com/ and create an app.
    This will give you an application ID a secret key to give as parameter here.

    By default, this script assumes that the redirect URL of the Deezer app is
    http://localhost:8080/oauth/return. If you use a different hostname and port,
    use the appropriate options.
    """
    # Start local webserver
    webserver = HTTPServer((hostname, port), MyServer)
    webserver.RequestHandlerClass.write_env = write_env
    webserver.RequestHandlerClass.variable_name = env_var_name

    # Commence OAuth Dance
    webserver.oauth_dancer = OAuthDancer(
        app_id=app_id,
        app_secret=app_secret,
        hostname=hostname,
        port=port,
    )
    start_url = webserver.oauth_dancer.get_auth_page()
    print(f"Opening {start_url} in web browser...")
    webbrowser.open(start_url)

    # Wait for user action and display token when finished
    try:
        webserver.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        webserver.server_close()


class OAuthDancer:
    """A class to help with completing the OAuth dance."""

    base_url: str = "https://connect.deezer.com"
    app_id: str
    app_secret: str

    def __init__(self, app_id: str, app_secret: str, hostname: str, port: int) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.hostname = hostname
        self.port = port

    @property
    def redirect_url(self) -> str:
        return f"http://{self.hostname}:{self.port}{REDIRECT_PATH}"

    def get_auth_page(self) -> str:
        """Build the URL of the auth page where the process starts."""
        query = urlencode(
            {
                "app_id": self.app_id,
                "redirect_uri": self.redirect_url,
                "perms": ",".join(
                    [
                        "basic_access",
                        "email",
                        "manage_library",
                        "delete_library",
                        "listening_history",
                    ]
                ),
            }
        )
        return f"{self.base_url}/oauth/auth.php?{query}"

    def get_token(self, code: str) -> dict[str, str]:
        """Make the API call to obtain the token."""
        query = urlencode(
            {
                "app_id": self.app_id,
                "secret": self.app_secret,
                "code": code,
            }
        )
        url = f"{self.base_url}/oauth/access_token.php?{query}"
        response = requests.get(url)
        content = response.content.decode()
        # The body looks like this: 'access_token=blah&expires=1234'
        # -> parse this to a dictionary
        return dict(tuple(p.split("=", 1)) for p in content.split("&"))


def render_page(lines: list[str], links: dict[str, str]) -> str:
    template_path = Path(__file__).parent / "page_template.html"
    template = Template(template_path.read_text(), autoescape=True)
    return template.render(lines=lines, links=links)


class MyServer(BaseHTTPRequestHandler):
    """Simple HTTP request handler to perform the OAuth dance."""

    write_env: bool
    variable_name: str

    def do_GET(self) -> None:
        """Route GET requests to the right handler."""
        if self.path.startswith(REDIRECT_PATH):
            self.redirect_route()
        else:
            self._write_response(
                links={"Start Oauth Flow": self.oauth_dancer.get_auth_page()}
            )

    def redirect_route(self) -> None:
        """
        Handle the redirect route.
        Once the OAuth is approved, Deezer redirects to this route with `?code=blah`
        at the end of the URL.
        Grab this code, make the API call to obtain the token and display it.
        """
        route, params_str = self.path.split("?", 1)
        query_params = dict(p.split("=", 1) for p in params_str.split("&"))
        token_data = self.oauth_dancer.get_token(query_params["code"])
        self._write_response(
            lines=[
                f"Token = {token_data['access_token']}",
                f"Expires = {token_data['expires']}",
            ]
        )

        # Write token to .env file
        access_token = token_data["access_token"]
        if self.write_env:
            env_path = Path(".env")
            if env_path.exists():
                content = env_path.read_text()
                token_re = re.compile(fr"^{self.variable_name}=.*$")
                if token_re.search(content):
                    content = token_re.sub(
                        f"{self.variable_name}={access_token}", content
                    )
                else:
                    content = f"{content}\n{self.variable_name}={access_token}"
            else:
                content = f"{self.variable_name}={access_token}\n"

            env_path.write_text(content)
            print("API token saved to .env file")
        else:
            print(f"{self.variable_name}={access_token}")
        raise SystemExit("All Done")

    def _write_response(
        self,
        lines: list[str] | None = None,
        links: dict[str, str] | None = None,
    ):
        """Build the HTTP response with appropriate content."""
        lines = lines or []
        links = links or {}
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(render_page(lines, links).encode())

    @property
    def oauth_dancer(self):
        """Shortcut to access the `OAuthDancer` instance."""
        return self.server.oauth_dancer
