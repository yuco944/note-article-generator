"""
Test suite for Health API endpoint
"""
import pytest
from app.main import create_app


@pytest.fixture
def client():
    """Flask test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test GET /api/v1/health endpoint"""
    response = client.get('/api/v1/health')

    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    assert 'version' in response.json


def test_health_endpoint_has_correct_structure(client):
    """Test health endpoint response structure"""
    response = client.get('/api/v1/health')
    data = response.json

    # 必須フィールドの確認
    required_fields = ['status', 'version']
    for field in required_fields:
        assert field in data, f'{field} should be in response'

    # statusの値確認
    assert data['status'] == 'ok'

    # versionの形式確認（x.y.z）
    version = data['version']
    assert isinstance(version, str)
    assert len(version.split('.')) == 3
