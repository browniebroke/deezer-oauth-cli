from __future__ import annotations


def write_env_file(access_token: str) -> None:
    """Write token to .env file."""
    with open(".env", "w+") as file:
        file.writelines(["API_TOKEN=" + access_token + "\n"])
        print("Token written to .env file")
