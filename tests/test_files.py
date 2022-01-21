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

    @pytest.mark.parametrize(
        ("before", "after"),
        [
            (
                "SOMETHING=test\n",
                "SOMETHING=test\nAPI_TOKEN=new\n",
            ),
            (
                "SOMETHING=test\nAPI_TOKEN=old\n",
                "SOMETHING=test\nAPI_TOKEN=new\n",
            ),
            (
                "OTHER_API_TOKEN=test\nAPI_TOKEN=old\n",
                "OTHER_API_TOKEN=test\nAPI_TOKEN=new\n",
            ),
            (
                "API_TOKEN=old\nTHING=test",
                "API_TOKEN=new\nTHING=test\n",
            ),
            (
                "API_TOKEN=old\n",
                "API_TOKEN=new\n",
            ),
            (
                "API_TOKEN=old",
                "API_TOKEN=new\n",
            ),
        ],
    )
    def test_update(self, workspace, before, after):
        env_file = workspace / ".env"
        env_file.write(before, "w")
        write_env_file("new")
        assert env_file.exists()
        assert env_file.read_text("utf-8") == after
