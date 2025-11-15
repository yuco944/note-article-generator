"""
Note API
記事生成・履歴取得のエンドポイント
"""
from flask import Blueprint, request, jsonify
from app.services.note_service import NoteService
from app.models.errors import ValidationError, TokenLimitExceededError

# Blueprintの作成
notes_bp = Blueprint('notes', __name__)

# サービスのインスタンス化
note_service = NoteService()


@notes_bp.route('/api/v1/notes/generate', methods=['POST'])
def generate_note():
    """
    記事生成エンドポイント

    Request Body:
        {
            "topic": str,
            "audience": str,
            "goal": str,
            "article_type": str,
            "length_class": str,
            "temperature": float,
            "intensity_level": int
        }

    Returns:
        JSON: 生成結果
    """
    try:
        # リクエストボディの取得
        request_data = request.get_json()

        if not request_data:
            raise ValidationError(
                message='リクエストボディが必要です',
                details={}
            )

        # 記事生成
        response = note_service.generate_note(request_data)

        # レスポンス返却
        return jsonify(response.to_dict()), 200

    except ValidationError as e:
        return e.to_response()
    except TokenLimitExceededError as e:
        return e.to_response()
    except Exception as e:
        # 予期しないエラー
        from app.models.errors import InternalError
        error = InternalError(
            message='予期しないエラーが発生しました',
            details={'error': str(e)}
        )
        return error.to_response()


@notes_bp.route('/api/v1/notes', methods=['GET'])
def list_notes():
    """
    記事履歴一覧取得エンドポイント

    Returns:
        JSON: 記事履歴
    """
    # TODO: Google Sheets から履歴を取得する実装
    # v1ではダミーデータを返す

    dummy_data = {
        'items': [
            {
                'note_id': 'note_20251115_0001',
                'title': 'サンプル記事1',
                'created_at': '2025-11-15T12:34:56Z',
                'article_type': 'education',
                'intensity_level': 7,
                'total_tokens': 3000
            },
            {
                'note_id': 'note_20251115_0002',
                'title': 'サンプル記事2',
                'created_at': '2025-11-15T13:45:12Z',
                'article_type': 'story',
                'intensity_level': 5,
                'total_tokens': 2500
            }
        ]
    }

    return jsonify(dummy_data), 200
