"""
Test suite for Note Service
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.note_service import NoteService
from app.models.errors import TokenLimitExceededError, ValidationError


class TestNoteService:
    """Tests for NoteService class"""

    @patch('app.clients.gsheet_client.GoogleSheetsClient')
    @patch('app.clients.llm_client.call_agent2')
    @patch('app.clients.llm_client.call_agent1')
    def test_generate_note_success(self, mock_agent1, mock_agent2, mock_gsheet_class):
        """Test successful note generation"""
        # Mock Google Sheets client class
        mock_client = MagicMock()
        mock_client.service = MagicMock()  # Initialize service
        mock_client.get_total_tokens_this_month.return_value = 0
        mock_client.append_row.return_value = True
        mock_gsheet_class.return_value = mock_client

        # Agent1のレスポンス
        agent1_response = {
            'title': 'Agent1タイトル',
            'lead': 'Agent1リード',
            'sections': [
                {'heading': '■見出し1', 'body': '本文1'},
                {'heading': '■見出し2', 'body': '本文2'}
            ],
            'cta': 'Agent1 CTA',
            'token_usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 2000,
                'total_tokens': 3000
            }
        }
        mock_agent1.return_value = agent1_response

        # Agent2のレスポンス
        agent2_response = {
            'title': 'Agent2タイトル',
            'lead': 'Agent2リード',
            'sections': [
                {'heading': '■調整後見出し1', 'body': '調整後本文1'},
                {'heading': '■調整後見出し2', 'body': '調整後本文2'}
            ],
            'cta': 'Agent2 CTA',
            'token_usage': {
                'prompt_tokens': 1500,
                'completion_tokens': 3500,
                'total_tokens': 5000
            }
        }
        mock_agent2.return_value = agent2_response

        request_data = {
            'topic': 'AI副業',
            'audience': '副業初心者',
            'goal': '稼ぎ方を教える',
            'article_type': 'education',
            'length_class': 'middle',
            'temperature': 0.8,
            'intensity_level': 7
        }

        service = NoteService()
        result = service.generate_note(request_data)

        # Agent1が呼ばれた
        mock_agent1.assert_called_once()

        # Agent2が呼ばれた
        mock_agent2.assert_called_once_with(agent1_response)

        # 結果の検証
        assert result.title == 'Agent2タイトル'
        assert result.lead == 'Agent2リード'
        assert len(result.sections) == 2
        assert result.cta == 'Agent2 CTA'
        assert result.note_id is not None
        assert result.metadata['topic'] == 'AI副業'
        assert result.metadata['token_usage']['total_tokens'] == 5000

        # ログ保存が呼ばれた
        mock_client.append_row.assert_called_once()
    
    @patch('app.clients.gsheet_client.GoogleSheetsClient')
    @patch('app.clients.llm_client.call_agent1')
    def test_generate_note_token_limit_exceeded(self, mock_agent1, mock_gsheet_class):
        """Test note generation when token limit exceeded"""
        mock_client = MagicMock()
        mock_client.service = MagicMock()  # Initialize service
        mock_client.get_total_tokens_this_month.return_value = 298000
        mock_gsheet_class.return_value = mock_client

        request_data = {
            'topic': 'test',
            'audience': 'test',
            'goal': 'test',
            'length_class': 'middle'  # 推定3000トークン → 298000 + 3000 > 300000
        }

        service = NoteService()

        with pytest.raises(TokenLimitExceededError) as exc_info:
            service.generate_note(request_data)

        assert '月次トークン上限を超過します' in str(exc_info.value)

        # LLM APIは呼ばれない（トークンチェックで失敗するため）
        mock_agent1.assert_not_called()
    
    def test_generate_note_validation_error(self):
        """Test note generation with invalid request"""
        service = NoteService()

        request_data = {
            'topic': '',  # 空のtopic
            'audience': 'test',
            'goal': 'test'
        }

        with pytest.raises(ValidationError):
            service.generate_note(request_data)
    
    @patch('app.clients.gsheet_client.GoogleSheetsClient')
    @patch('app.clients.llm_client.call_agent2')
    @patch('app.clients.llm_client.call_agent1')
    def test_generate_note_default_values(self, mock_agent1, mock_agent2, mock_gsheet_class):
        """Test note generation with default parameter values"""
        # Mock Google Sheets client class
        mock_client = MagicMock()
        mock_client.service = MagicMock()  # Initialize service
        mock_client.get_total_tokens_this_month.return_value = 0
        mock_client.append_row.return_value = True
        mock_gsheet_class.return_value = mock_client

        agent1_response = {
            'title': 'テスト',
            'lead': 'テスト',
            'sections': [],
            'cta': 'テスト',
            'token_usage': {'prompt_tokens': 100, 'completion_tokens': 200, 'total_tokens': 300}
        }
        mock_agent1.return_value = agent1_response

        agent2_response = {
            'title': 'テスト',
            'lead': 'テスト',
            'sections': [],
            'cta': 'テスト',
            'token_usage': {'prompt_tokens': 150, 'completion_tokens': 250, 'total_tokens': 400}
        }
        mock_agent2.return_value = agent2_response

        # 最低限のパラメータのみ
        request_data = {
            'topic': 'test',
            'audience': 'test',
            'goal': 'test'
        }

        service = NoteService()
        result = service.generate_note(request_data)

        # デフォルト値が設定されている
        assert result.metadata['article_type'] == 'education'
        assert result.metadata['length_class'] == 'middle'
        assert result.metadata['temperature_used'] == 0.7
        assert result.metadata['intensity_level_used'] == 5
