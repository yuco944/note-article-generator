"""
エラー定義
APIエラーレスポンスの標準化
"""
from flask import jsonify


class APIError(Exception):
    """API基底エラークラス"""

    def __init__(self, code, message, details=None, status_code=400):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        """エラー情報を辞書に変換"""
        return {
            'error': {
                'code': self.code,
                'message': self.message,
                'details': self.details
            }
        }

    def to_response(self):
        """Flaskレスポンスに変換"""
        response = jsonify(self.to_dict())
        response.status_code = self.status_code
        return response


class ValidationError(APIError):
    """バリデーションエラー"""

    def __init__(self, message, details=None):
        super().__init__(
            code='VALIDATION_ERROR',
            message=message,
            details=details,
            status_code=400
        )


class TokenLimitExceededError(APIError):
    """トークン上限超過エラー"""

    def __init__(self, message='月次トークン上限を超過しています', details=None):
        super().__init__(
            code='TOKEN_LIMIT_EXCEEDED',
            message=message,
            details=details,
            status_code=429
        )


class UnauthorizedError(APIError):
    """認証エラー"""

    def __init__(self, message='認証に失敗しました', details=None):
        super().__init__(
            code='UNAUTHORIZED',
            message=message,
            details=details,
            status_code=401
        )


class InternalError(APIError):
    """内部エラー"""

    def __init__(self, message='サーバー内部エラーが発生しました', details=None):
        super().__init__(
            code='INTERNAL_ERROR',
            message=message,
            details=details,
            status_code=500
        )


def register_error_handlers(app):
    """Flaskアプリにエラーハンドラーを登録"""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """API

エラーのハンドリング"""
        return error.to_response()

    @app.errorhandler(404)
    def handle_not_found(error):
        """404エラーのハンドリング"""
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': '指定されたリソースが見つかりません',
                'details': {}
            }
        }), 404

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """500エラーのハンドリング"""
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'サーバー内部エラーが発生しました',
                'details': {}
            }
        }), 500
