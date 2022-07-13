"""Simple script to obtain an API token via OAuth."""
from __future__ import annotations

import webbrowser

import typer
from rich import print

from deezer_oauth.client import OAuthDancer
from deezer_oauth.server import run_server

app = typer.Typer()


@app.command()
def main(app_id: str, app_secret: str) -> None:
    """
    Obtain an API token from Deezer.

    This script spins up a basic HTTP server, perform the OAuth flow to generate
    an API token and write it to an .env file in the local directory.

    You should log in/signup at https://developers.deezer.com/ and create an app
    with a redirect URL of 'http://localhost:8080/oauth/return'.

    This will give you an application ID a secret key to give as parameter here.
    """
    # Commence OAuth flow
    oauth_dancer = OAuthDancer(app_id=app_id, app_secret=app_secret)
    start_url = oauth_dancer.get_auth_page()
    print(f"Opening {start_url} in web browser...")
    webbrowser.open(start_url)

    # Run server until flow complete
    run_server(oauth_dancer)
