import subprocess
from typing import List


def run_command(command: List[str]) -> str:
    """Run a command on the mainframe host via SSH.

    This is a placeholder implementation. Replace it with an appropriate
    automation library such as py3270 or paramiko for production use.
    """
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout
