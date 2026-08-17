import pytest

from app import app as flask_app


@pytest.fixture
def client():
    """A Flask test client backed by the real seeded database."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as test_client:
        yield test_client
