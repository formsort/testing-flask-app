import pytest


@pytest.fixture
def get_root(client):
    def _get_root():
        return client.get("/")

    return _get_root


def test_root(get_root):
    resp = get_root()
    assert resp.status_code < 400
    assert resp.data
    assert resp.content_type.startswith("text/html")
