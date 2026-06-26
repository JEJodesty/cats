import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLEAN_SCRIPT = REPO_ROOT / "scripts" / "clean-test-data.sh"


def clean_test_data() -> None:
    if not CLEAN_SCRIPT.is_file():
        raise FileNotFoundError(f"Missing cleanup script: {CLEAN_SCRIPT}")
    subprocess.run(["bash", str(CLEAN_SCRIPT)], check=True, cwd=REPO_ROOT)


@pytest.fixture(scope="session", autouse=True)
def clean_test_data_fixture():
    clean_test_data()
