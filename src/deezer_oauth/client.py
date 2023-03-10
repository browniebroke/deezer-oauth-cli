from __future__ import annotations

from urllib.parse import parse_qsl, urlencode

import requests

from deezer_oauth.constants import HOST_NAME, OAUTH_RETURN_PATH, SERVER_PORT


class OAuthDancer:
    """A class to help with completing the OAuth dance."""

    base_url: str = "https://connect.deezer.com"
    app_id: str
    app_secret: str
    redirect_url: str = f"http://{HOST_NAME}:{SERVER_PORT}{OAUTH_RETURN_PATH}"

    def __init__(self, app_id: str, app_secret: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret

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
                        "manage_community",
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
        response = requests.get(url, timeout=10)
        content = response.content.decode()
        # The body looks like this: 'access_token=blah&expires=1234'
        # -> parse this as querystring and convert to a dictionary
        return dict(parse_qsl(content))
