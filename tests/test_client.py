import responses

from deezer_oauth.client import OAuthDancer


class TestOAuthDancer:
    def test_get_auth_page(self):
        dancer = OAuthDancer(app_id="1234", app_secret="dzr-secret")
        url = dancer.get_auth_page()
        assert url == (
            "https://connect.deezer.com/oauth/auth.php"
            "?app_id=1234"
            "&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foauth%2Freturn"
            "&perms=basic_access%2Cemail%2Cmanage_library"
            "%2Cdelete_library%2Clistening_history"
        )

    @responses.activate
    def test_get_token(self):
        responses.add(
            responses.GET,
            "https://connect.deezer.com/oauth/access_token.php",
            body="access_token=blah&expires=1234",
        )
        dancer = OAuthDancer(app_id="abcd", app_secret="secret")
        result = dancer.get_token("my-personal-code")
        assert result == {"access_token": "blah", "expires": "1234"}
