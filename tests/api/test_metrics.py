import pytest


@pytest.mark.django_db
def test_create_metric_record(auth_client, test_metric, test_tag):
    url = f"/api/metrics/{test_metric.id}/records/"

    data = {
        "value": 100.5,
        "tags": [test_tag.id]
    }

    response = auth_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['value'] == 100.5
    assert len(response.data['tags']) == 1


@pytest.mark.django_db
def test_create_record_unauthorized(api_client, test_metric):
    url = f"/api/metrics/{test_metric.id}/records/"
    response = api_client.post(url, {"value": 10}, format='json')

    assert response.status_code == 401
