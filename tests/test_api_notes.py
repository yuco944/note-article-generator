"""
Test suite for Notes API endpoints
"""
import pytest
from unittest.mock import patch, MagicMock
from app.main import create_app


@pytest.fixture
def client():
    """Flask test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_request_payload():
    """Valid request payload for note generation"""
    return {
        'topic': 'AI副業で月5万円稼ぐ方法',
        'audience': '副業初心者',
        'goal': '具体的な稼ぎ方を教える',
        'article_type': 'education',
        'length_class': 'middle',
        'temperature': 0.8,
        'intensity_level': 7
    }


@pytest.fixture
def mock_note_response():
    """Mock note generation response"""
    return {
        'note_id': 'TEST123456',
        'title': 'テストタイトル',
        'lead': 'テストリード文',
        'sections': [
            {'heading': '■見出し1', 'body': '本文1'},
            {'heading': '■見出し2', 'body': '本文2'},
            {'heading': '■見出し3', 'body': '本文3'}
        ],
        'cta': 'テストCTA',
        'metadata': {
            'topic': 'AI副業で月5万円稼ぐ方法',
            'audience': '副業初心者',
            'goal': '具体的な稼ぎ方を教える',
            'article_type': 'education',
            'length_class': 'middle',
            'temperature': 0.8,
            'intensity_level': 7,
            'created_at': '2025-01-01T00:00:00',
            'token_usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 2000,
                'total_tokens': 3000
            }
        }
    }


class TestNotesGenerate:
    """Tests for POST /api/v1/notes/generate endpoint"""

    @patch('app.services.note_service.NoteService.generate_note')
    def test_generate_note_success(self, mock_generate, client, valid_request_payload, mock_note_response):
        """Test successful note generation"""
        from app.models.note_models import GenerateNoteResponse, NoteSection

        # Mock the response as a GenerateNoteResponse object
        response_obj = GenerateNoteResponse(
            status='SUCCESS',
            note_id='TEST123456',
            title='テストタイトル',
            lead='テストリード文',
            sections=[
                NoteSection(heading='■見出し1', body='本文1'),
                NoteSection(heading='■見出し2', body='本文2'),
                NoteSection(heading='■見出し3', body='本文3')
            ],
            cta='テストCTA',
            metadata=mock_note_response['metadata']
        )
        mock_generate.return_value = response_obj

        response = client.post(
            '/api/v1/notes/generate',
            json=valid_request_payload,
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.json['note_id'] == 'TEST123456'
        assert response.json['title'] == 'テストタイトル'
        assert len(response.json['sections']) == 3
    
    def test_generate_note_missing_required_field(self, client):
        """Test validation error for missing required field"""
        invalid_payload = {
            'audience': '副業初心者',
            'goal': '具体的な稼ぎ方を教える'
            # topicが欠落
        }
        
        response = client.post(
            '/api/v1/notes/generate',
            json=invalid_payload,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_generate_note_invalid_temperature(self, client, valid_request_payload):
        """Test validation error for invalid temperature"""
        invalid_payload = valid_request_payload.copy()
        invalid_payload['temperature'] = 3.0  # 範囲外（0.0-2.0）
        
        response = client.post(
            '/api/v1/notes/generate',
            json=invalid_payload,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_generate_note_invalid_intensity_level(self, client, valid_request_payload):
        """Test validation error for invalid intensity_level"""
        invalid_payload = valid_request_payload.copy()
        invalid_payload['intensity_level'] = 15  # 範囲外（1-10）
        
        response = client.post(
            '/api/v1/notes/generate',
            json=invalid_payload,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_generate_note_invalid_article_type(self, client, valid_request_payload):
        """Test validation error for invalid article_type"""
        invalid_payload = valid_request_payload.copy()
        invalid_payload['article_type'] = 'invalid_type'
        
        response = client.post(
            '/api/v1/notes/generate',
            json=invalid_payload,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_generate_note_invalid_length_class(self, client, valid_request_payload):
        """Test validation error for invalid length_class"""
        invalid_payload = valid_request_payload.copy()
        invalid_payload['length_class'] = 'invalid_length'
        
        response = client.post(
            '/api/v1/notes/generate',
            json=invalid_payload,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json


class TestNotesIndex:
    """Tests for GET /api/v1/notes endpoint"""

    def test_get_notes_returns_dummy_data(self, client):
        """Test notes endpoint returns dummy data (current implementation)"""
        response = client.get('/api/v1/notes')

        assert response.status_code == 200
        assert 'items' in response.json
        assert isinstance(response.json['items'], list)
