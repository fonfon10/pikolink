import subprocess
import sys

def main() -> None:
    raise SystemExit(
        subprocess.call([sys.executable, "manage.py", "test"])
    )