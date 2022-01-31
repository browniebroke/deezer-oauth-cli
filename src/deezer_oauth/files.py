from __future__ import annotations

import re
from pathlib import Path


def write_env_file(access_token: str) -> None:
    """Write token to .env file."""
    variable_name = "API_TOKEN"
    line_to_insert = f"{variable_name}={access_token}"
    env_path = Path(".env")
    if env_path.exists():
        pattern = re.compile(rf"^{variable_name}=.*$")
        content = env_path.read_text()
        updated_lines = []
        inserted = False
        original_lines = content.split("\n")
        # breakpoint()
        for line in original_lines:
            if not line:
                continue
            if pattern.match(line):
                updated_lines.append(line_to_insert)
                inserted = True
            else:
                updated_lines.append(line)
        if not inserted:
            updated_lines.append(line_to_insert)
        updated_content = "\n".join(updated_lines)
    else:
        updated_content = line_to_insert
    env_path.write_text(f"{updated_content}\n")
