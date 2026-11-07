from __future__ import annotations

from typing import TYPE_CHECKING

from deezer_oauth.client import OAuthDancer

if TYPE_CHECKING:
    import respx


class TestOAuthDancer:
    def test_get_auth_page(self) -> None:
        dancer = OAuthDancer(app_id="1234", app_secret="dzr-secret")  # noqa S106
        url = dancer.get_auth_page()
        assert url == (
            "https://connect.deezer.com/oauth/auth.php"
            "?app_id=1234"
            "&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foauth%2Freturn"
            "&perms=basic_access%2Cemail%2Cmanage_library%2Cmanage_community"
            "%2Cdelete_library%2Clistening_history"
        )

    def test_get_token(self, httpx2_mock: respx.MockRouter) -> None:
        get_token_route: respx.Route = httpx2_mock.get(
            "https://connect.deezer.com/oauth/access_token.php"
        )
        get_token_route.respond(200, text="access_token=blah&expires=1234")
        dancer = OAuthDancer(app_id="abcd", app_secret="secret")  # noqa S106
        result = dancer.get_token("my-personal-code")
        assert result == {"access_token": "blah", "expires": "1234"}
        assert get_token_route.call_count == 1
