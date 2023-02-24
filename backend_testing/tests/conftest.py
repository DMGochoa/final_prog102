from shutil import copy

import pytest
from bank_api.api import create_app
from bank_api.constants import BANK_DATABASE, PROJECT_ROOT


@pytest.fixture
def client(tmpdir):
    copy(f"{PROJECT_ROOT}/{BANK_DATABASE}", tmpdir.dirpath())

    temp_db_file = f"sqlite:///{tmpdir.dirpath()}/{BANK_DATABASE}"

    app = create_app(temp_db_file)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client