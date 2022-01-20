import os

import pytest

from deezer_oauth.files import write_env_file


@pytest.fixture
def workspace(tmpdir):
    cwd = os.getcwd()
    os.chdir(tmpdir)
    yield tmpdir
    os.chdir(cwd)


class TestWriteEnvFile:
    def test_create(self, workspace):
        env_file = workspace / ".env"
        write_env_file("qwerty")
        assert env_file.exists()
        assert env_file.read_text("utf-8") == "API_TOKEN=qwerty\n"

    def test_existing(self, workspace):
        env_file = workspace / ".env"
        env_file.write("SOMETHING=test\n", "w")
        write_env_file("uiop")
        assert env_file.exists()
        assert env_file.read_text("utf-8") == "API_TOKEN=uiop\n"
