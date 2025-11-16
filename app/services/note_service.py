"""
Note生成サービス
記事生成のビジネスロジックを担当
"""
import json
from datetime import datetime
from app.models.note_models import (
    GenerateNoteRequest,
    GenerateNoteResponse,
    NoteSection,
    TokenUsage,
    NoteLogEntry,
    generate_note_id
)
from app.models.errors import ValidationError, InternalError
from app.clients import llm_client
from app.clients.gsheet_client import get_gsheet_client
from app.services.token_service import TokenService


class NoteService:
    """Note生成サービス"""

    def __init__(self):
        """初期化"""
        self.gsheet_client = get_gsheet_client()
        self.token_service = TokenService()

    def generate_note(self, request_data: dict) -> GenerateNoteResponse:
        """
        note記事を生成

        Args:
            request_data: リクエストデータ

        Returns:
            GenerateNoteResponse: 生成結果

        Raises:
            ValidationError: バリデーションエラー
            InternalError: 内部エラー
        """
        try:
            # 1. リクエストのバリデーション
            request = self._validate_request(request_data)

            # 2. トークン制限チェック（推定値）
            estimated_tokens = self._estimate_tokens(request)
            self.token_service.check_token_limit(estimated_tokens)

            # 3. note_idの生成
            note_id = generate_note_id()

            # 4. Agent1でドラフト生成
            agent1_payload = {
                'topic': request.topic,
                'audience': request.audience,
                'goal': request.goal,
                'article_type': request.article_type,
                'length_class': request.length_class,
                'temperature': request.temperature,
                'intensity_level': request.intensity_level
            }

            agent1_result = llm_client.call_agent1(agent1_payload)

            # 5. Agent2で文体調整
            agent2_result = llm_client.call_agent2(agent1_result)

            # 6. レスポンスの構築
            response = self._build_response(
                note_id=note_id,
                request=request,
                result=agent2_result
            )

            # 7. Google Sheetsに保存
            self._save_to_gsheet(request, response)

            return response

        except ValidationError:
            raise
        except Exception as e:
            # 詳細なエラーログを出力
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌❌❌ 記事生成エラー詳細 ❌❌❌")
            print(f"エラー: {e}")
            print(f"トレースバック:\n{error_trace}")
            print(f"❌❌❌❌❌❌❌❌❌❌❌❌❌❌")

            raise InternalError(
                message='記事生成中にエラーが発生しました',
                details={'error': str(e), 'traceback': error_trace}
            )

    def _validate_request(self, request_data: dict) -> GenerateNoteRequest:
        """
        リクエストのバリデーション

        Args:
            request_data: リクエストデータ

        Returns:
            GenerateNoteRequest: バリデーション済みリクエスト

        Raises:
            ValidationError: バリデーションエラー
        """
        # 必須フィールドのデフォルト値設定
        request = GenerateNoteRequest(
            topic=request_data.get('topic', ''),
            audience=request_data.get('audience', ''),
            goal=request_data.get('goal', ''),
            article_type=request_data.get('article_type', 'education'),
            length_class=request_data.get('length_class', 'middle'),
            temperature=float(request_data.get('temperature', 0.7)),
            intensity_level=int(request_data.get('intensity_level', 5))
        )

        # バリデーション実行
        errors = request.validate()

        if errors:
            raise ValidationError(
                message='リクエストのバリデーションに失敗しました',
                details={'errors': errors}
            )

        return request

    def _build_response(
        self,
        note_id: str,
        request: GenerateNoteRequest,
        result: dict
    ) -> GenerateNoteResponse:
        """
        レスポンスの構築

        Args:
            note_id: 生成されたnote_id
            request: リクエスト
            result: LLM生成結果

        Returns:
            GenerateNoteResponse: レスポンス
        """
        # セクションの変換
        sections = [
            NoteSection(
                heading=section['heading'],
                body=section['body']
            )
            for section in result.get('sections', [])
        ]

        # トークン使用量
        token_usage_data = result.get('token_usage', {})
        token_usage = TokenUsage(
            prompt_tokens=token_usage_data.get('prompt_tokens', 0),
            completion_tokens=token_usage_data.get('completion_tokens', 0),
            total_tokens=token_usage_data.get('total_tokens', 0)
        )

        # メタデータ
        metadata = {
            'topic': request.topic,
            'audience': request.audience,
            'goal': request.goal,
            'article_type': request.article_type,
            'length_class': request.length_class,
            'temperature_used': request.temperature,
            'intensity_level_used': request.intensity_level,
            'token_usage': token_usage.to_dict()
        }

        # レスポンス構築
        response = GenerateNoteResponse(
            status='SUCCESS',
            note_id=note_id,
            title=result.get('title', ''),
            lead=result.get('lead', ''),
            sections=sections,
            cta=result.get('cta', ''),
            metadata=metadata
        )

        return response

    def _estimate_tokens(self, request: GenerateNoteRequest) -> int:
        """
        トークン使用量の推定

        Args:
            request: リクエスト

        Returns:
            int: 推定トークン数
        """
        # 簡易推定：length_classに基づく
        estimates = {
            'short': 1500,
            'middle': 3000,
            'long': 5000
        }
        return estimates.get(request.length_class, 3000)

    def _save_to_gsheet(self, request: GenerateNoteRequest, response: GenerateNoteResponse):
        """
        Google Sheetsに保存

        Args:
            request: リクエスト
            response: レスポンス
        """
        try:
            # NoteLogEntry作成
            log_entry = NoteLogEntry(
                note_id=response.note_id,
                topic=request.topic,
                audience=request.audience,
                goal=request.goal,
                article_type=request.article_type,
                length_class=request.length_class,
                temperature=request.temperature,
                intensity_level=request.intensity_level,
                title=response.title,
                raw_json=json.dumps(response.to_dict(), ensure_ascii=False),
                total_tokens=response.metadata['token_usage']['total_tokens'],
                created_at=datetime.now().isoformat()
            )

            # Google Sheetsに保存
            self.gsheet_client.append_row(log_entry)

        except Exception as e:
            # 保存エラーは警告のみ（処理は続行）
            print(f"⚠️  Google Sheets保存エラー: {e}")
