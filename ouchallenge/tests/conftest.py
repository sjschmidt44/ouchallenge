import os
import pytest

ROOT_PATH = os.path.dirname(__file__)


@pytest.fixture()
def app():
    from ouchallenge import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)
