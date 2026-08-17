"""Integration tests for the adoption-status filter on GET /api/dogs.

These run against the real seeded database rather than mocks, which is what
lets them catch a filter that silently does nothing.
"""


def test_available_filter_excludes_adopted(client):
    resp = client.get('/api/dogs?status=AVAILABLE&per_page=100')
    assert resp.status_code == 200
    statuses = {d['status'] for d in resp.get_json()['dogs']}
    assert statuses <= {'AVAILABLE'}, f"filter leaked: {statuses}"


def test_no_filter_returns_everything(client):
    unfiltered = client.get('/api/dogs?per_page=100').get_json()
    explicit_all = client.get('/api/dogs?status=ALL&per_page=100').get_json()
    assert unfiltered['total'] == explicit_all['total']
    assert unfiltered['total'] > 0


def test_pagination_total_reflects_the_filter(client):
    everything = client.get('/api/dogs?per_page=100').get_json()
    available = client.get('/api/dogs?status=AVAILABLE&per_page=100').get_json()
    adopted = client.get('/api/dogs?status=ADOPTED&per_page=100').get_json()
    assert available['total'] + adopted['total'] <= everything['total']
    assert available['total'] < everything['total']


def test_unknown_status_returns_everything_without_erroring(client):
    resp = client.get('/api/dogs?status=banana&per_page=100')
    assert resp.status_code == 200
    everything = client.get('/api/dogs?per_page=100').get_json()
    assert resp.get_json()['total'] == everything['total']


def test_every_dog_carries_its_status(client):
    dogs = client.get('/api/dogs?per_page=100').get_json()['dogs']
    assert dogs
    assert all('status' in dog for dog in dogs)
