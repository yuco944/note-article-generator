"""
Test suite for LLM Client
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from app.clients.llm_client import (
    call_agent1,
    call_agent2,
    _extract_json_from_response
)


class TestExtractJsonFromResponse:
    """Tests for JSON extraction from LLM responses"""
    
    def test_extract_plain_json(self):
        """Test extracting plain JSON"""
        content = '{"title": "test", "lead": "test lead"}'
        result = _extract_json_from_response(content)
        
        assert result['title'] == 'test'
        assert result['lead'] == 'test lead'
    
    def test_extract_json_from_code_block(self):
        """Test extracting JSON from ```json code block"""
        content = '''Here is the result:
```json
{
  "title": "test",
  "lead": "test lead"
}
```
'''
        result = _extract_json_from_response(content)
        
        assert result['title'] == 'test'
        assert result['lead'] == 'test lead'
    
    def test_extract_json_from_generic_code_block(self):
        """Test extracting JSON from ``` code block"""
        content = '''```
{
  "title": "test",
  "lead": "test lead"
}
```'''
        result = _extract_json_from_response(content)
        
        assert result['title'] == 'test'
        assert result['lead'] == 'test lead'
    
    def test_extract_json_from_text_with_json(self):
        """Test extracting JSON embedded in text"""
        content = 'Here is your article: {"title": "test", "lead": "test lead"} Hope this helps!'
        result = _extract_json_from_response(content)
        
        assert result['title'] == 'test'
        assert result['lead'] == 'test lead'
    
    def test_extract_json_invalid_content(self):
        """Test extraction failure with invalid content"""
        content = 'This is not JSON at all'
        
        with pytest.raises(ValueError) as exc_info:
            _extract_json_from_response(content)
        
        assert 'JSONを抽出できませんでした' in str(exc_info.value)


class TestCallAgent1:
    """Tests for Agent1 (draft generation)"""
    
    @patch('app.clients.llm_client._call_claude_api')
    @patch('app.clients.llm_client.config')
    def test_call_agent1_claude_success(self, mock_config, mock_claude_api):
        """Test successful Agent1 call with Claude"""
        mock_config.LLM_PROVIDER = 'claude'
        mock_config.LLM_AGENT1_MAX_TOKENS = 8000
        mock_config.LLM_MODEL_AGENT1 = 'claude-3-5-sonnet-20241022'
        
        mock_response = {
            'content': json.dumps({
                'title': 'テストタイトル',
                'lead': 'テストリード',
                'sections': [
                    {'heading': '■見出し1', 'body': '本文1'}
                ],
                'cta': 'テストCTA'
            }),
            'token_usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 2000,
                'total_tokens': 3000
            }
        }
        mock_claude_api.return_value = mock_response
        
        payload = {
            'topic': 'AI副業',
            'audience': '副業初心者',
            'goal': '稼ぎ方を教える',
            'article_type': 'education',
            'length_class': 'middle',
            'temperature': 0.8,
            'intensity_level': 7
        }
        
        result = call_agent1(payload)
        
        assert result['title'] == 'テストタイトル'
        assert result['lead'] == 'テストリード'
        assert len(result['sections']) == 1
        assert result['token_usage']['total_tokens'] == 3000
        
        # API呼び出しパラメータの確認
        mock_claude_api.assert_called_once()
        call_args = mock_claude_api.call_args
        assert call_args[1]['temperature'] == 0.8
        assert call_args[1]['max_tokens'] == 8000
    
    @patch('app.clients.llm_client._call_openai_api')
    @patch('app.clients.llm_client.config')
    def test_call_agent1_openai_success(self, mock_config, mock_openai_api):
        """Test successful Agent1 call with OpenAI"""
        mock_config.LLM_PROVIDER = 'openai'
        mock_config.LLM_AGENT1_MAX_TOKENS = 8000
        mock_config.LLM_MODEL_AGENT1 = 'gpt-4'
        
        mock_response = {
            'content': json.dumps({
                'title': 'テストタイトル',
                'lead': 'テストリード',
                'sections': [
                    {'heading': '■見出し1', 'body': '本文1'}
                ],
                'cta': 'テストCTA'
            }),
            'token_usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 2000,
                'total_tokens': 3000
            }
        }
        mock_openai_api.return_value = mock_response
        
        payload = {
            'topic': 'Python学習',
            'audience': 'プログラミング初心者',
            'goal': '基礎を教える',
            'temperature': 0.7
        }
        
        result = call_agent1(payload)
        
        assert result['title'] == 'テストタイトル'
        assert result['token_usage']['total_tokens'] == 3000
    
    @patch('app.clients.llm_client.config')
    def test_call_agent1_unsupported_provider(self, mock_config):
        """Test Agent1 call with unsupported provider"""
        mock_config.LLM_PROVIDER = 'invalid_provider'
        
        payload = {'topic': 'test'}
        
        with pytest.raises(ValueError) as exc_info:
            call_agent1(payload)
        
        assert 'Unsupported LLM provider' in str(exc_info.value)


class TestCallAgent2:
    """Tests for Agent2 (style adjustment)"""
    
    @patch('app.clients.llm_client._call_claude_api')
    @patch('app.clients.llm_client.config')
    def test_call_agent2_success(self, mock_config, mock_claude_api):
        """Test successful Agent2 call"""
        mock_config.LLM_PROVIDER = 'claude'
        mock_config.LLM_AGENT2_MAX_TOKENS = 8000
        mock_config.LLM_MODEL_AGENT2 = 'claude-3-5-sonnet-20241022'
        
        mock_response = {
            'content': json.dumps({
                'title': '調整後タイトル',
                'lead': '調整後リード',
                'sections': [
                    {'heading': '■調整後見出し1', 'body': '調整後本文1'}
                ],
                'cta': '調整後CTA'
            }),
            'token_usage': {
                'prompt_tokens': 500,
                'completion_tokens': 1500,
                'total_tokens': 2000
            }
        }
        mock_claude_api.return_value = mock_response
        
        agent1_result = {
            'title': '元タイトル',
            'lead': '元リード',
            'sections': [
                {'heading': '■元見出し1', 'body': '元本文1'}
            ],
            'cta': '元CTA',
            'token_usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 2000,
                'total_tokens': 3000
            }
        }
        
        result = call_agent2(agent1_result)
        
        assert result['title'] == '調整後タイトル'
        # トークン使用量が合算されている
        assert result['token_usage']['total_tokens'] == 5000
        assert result['token_usage']['prompt_tokens'] == 1500
        assert result['token_usage']['completion_tokens'] == 3500
        
        # temperature=0.3で呼ばれている
        call_args = mock_claude_api.call_args
        assert call_args[1]['temperature'] == 0.3
    
    @patch('app.clients.llm_client._call_claude_api')
    @patch('app.clients.llm_client.config')
    def test_call_agent2_without_previous_token_usage(self, mock_config, mock_claude_api):
        """Test Agent2 when Agent1 result has no token_usage"""
        mock_config.LLM_PROVIDER = 'claude'
        mock_config.LLM_AGENT2_MAX_TOKENS = 8000
        mock_config.LLM_MODEL_AGENT2 = 'claude-3-5-sonnet-20241022'
        
        mock_response = {
            'content': json.dumps({
                'title': '調整後タイトル',
                'lead': '調整後リード',
                'sections': [],
                'cta': '調整後CTA'
            }),
            'token_usage': {
                'prompt_tokens': 500,
                'completion_tokens': 1500,
                'total_tokens': 2000
            }
        }
        mock_claude_api.return_value = mock_response
        
        agent1_result = {
            'title': '元タイトル',
            'lead': '元リード',
            'sections': [],
            'cta': '元CTA'
            # token_usageが無い
        }
        
        result = call_agent2(agent1_result)
        
        # Agent2のトークン使用量のみ
        assert result['token_usage']['total_tokens'] == 2000
