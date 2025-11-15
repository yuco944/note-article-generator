"""
LLMクライアント
Claude / OpenAI APIを呼び出して記事生成を行う
"""
import json
import re
from app.config import get_config
from app.clients.llm_prompts import (
    AGENT1_SYSTEM_PROMPT,
    AGENT2_SYSTEM_PROMPT,
    build_agent1_user_prompt,
    build_agent2_user_prompt
)

config = get_config()


def call_agent1(payload: dict) -> dict:
    """
    構成＋ドラフト生成用のLLM呼び出し

    Args:
        payload: リクエストパラメータ（topic, audience, goal, etc.）

    Returns:
        dict: 生成結果
            - title: str
            - lead: str
            - sections: list[dict] - [{"heading": str, "body": str}]
            - cta: str
            - token_usage: dict - {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int}
    """
    # ユーザープロンプト構築
    user_prompt = build_agent1_user_prompt(payload)

    # temperature取得（0.0-2.0）
    temperature = float(payload.get('temperature', 0.7))

    # max_tokens設定
    max_tokens = config.LLM_AGENT1_MAX_TOKENS

    # LLMプロバイダに応じてAPI呼び出し
    if config.LLM_PROVIDER == 'claude':
        response = _call_claude_api(
            system_prompt=AGENT1_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            model=config.LLM_MODEL_AGENT1
        )
    elif config.LLM_PROVIDER == 'openai':
        response = _call_openai_api(
            system_prompt=AGENT1_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            model=config.LLM_MODEL_AGENT1
        )
    else:
        raise ValueError(f'Unsupported LLM provider: {config.LLM_PROVIDER}')

    # レスポンスからJSON抽出
    result = _extract_json_from_response(response['content'])

    # token_usage情報を追加
    result['token_usage'] = response['token_usage']

    return result


def call_agent2(payload: dict) -> dict:
    """
    Agent1の結果を受け、文体調整・禁止表現チェックをした最終版を返す

    Args:
        payload: Agent1の出力結果

    Returns:
        dict: 調整後の結果（Agent1と同じフォーマット）
    """
    # Agent2用のユーザープロンプト構築
    user_prompt = build_agent2_user_prompt(payload)

    # max_tokens設定
    max_tokens = config.LLM_AGENT2_MAX_TOKENS

    # temperature は低めに設定（文体調整のため）
    temperature = 0.3

    # LLMプロバイダに応じてAPI呼び出し
    if config.LLM_PROVIDER == 'claude':
        response = _call_claude_api(
            system_prompt=AGENT2_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            model=config.LLM_MODEL_AGENT2
        )
    elif config.LLM_PROVIDER == 'openai':
        response = _call_openai_api(
            system_prompt=AGENT2_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            model=config.LLM_MODEL_AGENT2
        )
    else:
        raise ValueError(f'Unsupported LLM provider: {config.LLM_PROVIDER}')

    # レスポンスからJSON抽出
    result = _extract_json_from_response(response['content'])

    # token_usage情報を元の情報と合算
    if 'token_usage' in payload:
        result['token_usage'] = {
            'prompt_tokens': payload['token_usage'].get('prompt_tokens', 0) + response['token_usage']['prompt_tokens'],
            'completion_tokens': payload['token_usage'].get('completion_tokens', 0) + response['token_usage']['completion_tokens'],
            'total_tokens': payload['token_usage'].get('total_tokens', 0) + response['token_usage']['total_tokens']
        }
    else:
        result['token_usage'] = response['token_usage']

    return result


def _call_claude_api(system_prompt: str, user_prompt: str, max_tokens: int,
                     temperature: float = 0.7, model: str = None) -> dict:
    """
    Claude APIを呼び出す

    Args:
        system_prompt: システムプロンプト
        user_prompt: ユーザープロンプト
        max_tokens: 最大トークン数
        temperature: 温度パラメータ（0.0-2.0）
        model: モデル名

    Returns:
        dict: API応答
            - content: str - 生成されたテキスト
            - token_usage: dict - トークン使用量
    """
    from anthropic import Anthropic

    client = Anthropic(api_key=config.LLM_API_KEY)

    if model is None:
        model = config.LLM_MODEL_AGENT1

    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # レスポンスから必要な情報を抽出
        content = response.content[0].text

        token_usage = {
            'prompt_tokens': response.usage.input_tokens,
            'completion_tokens': response.usage.output_tokens,
            'total_tokens': response.usage.input_tokens + response.usage.output_tokens
        }

        return {
            'content': content,
            'token_usage': token_usage
        }

    except Exception as e:
        print(f"❌ Claude API呼び出しエラー: {e}")
        raise


def _call_openai_api(system_prompt: str, user_prompt: str, max_tokens: int,
                     temperature: float = 0.7, model: str = None) -> dict:
    """
    OpenAI APIを呼び出す

    Args:
        system_prompt: システムプロンプト
        user_prompt: ユーザープロンプト
        max_tokens: 最大トークン数
        temperature: 温度パラメータ（0.0-2.0）
        model: モデル名

    Returns:
        dict: API応答
            - content: str - 生成されたテキスト
            - token_usage: dict - トークン使用量
    """
    from openai import OpenAI

    client = OpenAI(api_key=config.LLM_API_KEY)

    if model is None:
        model = 'gpt-4'

    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # レスポンスから必要な情報を抽出
        content = response.choices[0].message.content

        token_usage = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }

        return {
            'content': content,
            'token_usage': token_usage
        }

    except Exception as e:
        print(f"❌ OpenAI API呼び出しエラー: {e}")
        raise


def _extract_json_from_response(content: str) -> dict:
    """
    LLMの応答からJSON部分を抽出してパースする

    Args:
        content: LLMの応答テキスト

    Returns:
        dict: パースされたJSON

    Raises:
        ValueError: JSON抽出・パースに失敗した場合
    """
    # まずそのままJSONとしてパースを試みる
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # ```json ... ``` のコードブロックから抽出を試みる
    json_block_pattern = r'```json\s*([\s\S]*?)\s*```'
    match = re.search(json_block_pattern, content)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # ``` ... ``` のコードブロックから抽出を試みる
    code_block_pattern = r'```\s*([\s\S]*?)\s*```'
    match = re.search(code_block_pattern, content)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # { ... } の最初のJSON objectを抽出
    json_object_pattern = r'\{[\s\S]*\}'
    match = re.search(json_object_pattern, content)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # どの方法でも抽出できなかった場合はエラー
    print(f"⚠️  JSONの抽出に失敗しました。レスポンス内容:\n{content[:500]}...")
    raise ValueError('LLMの応答からJSONを抽出できませんでした')
