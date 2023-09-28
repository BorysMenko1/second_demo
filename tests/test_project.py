import pytest as pytest

from website import create_app

import pytest

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# ============= tests ===================

def test_not_null():
    assert "hello" is not None

def test_equals():
    assert 200==200

def test_not_equals():
    assert 200!=201
