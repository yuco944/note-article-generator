"""
トークン制限サービス
月次トークン使用量の管理
"""
from app.config import get_config
from app.models.errors import TokenLimitExceededError
from app.clients.gsheet_client import get_gsheet_client

config = get_config()


class TokenService:
    """トークン制限サービス"""

    def __init__(self):
        """初期化"""
        self.monthly_limit = config.MONTHLY_TOKEN_LIMIT
        self.gsheet_client = get_gsheet_client()

    def check_token_limit(self, estimated_tokens: int) -> bool:
        """
        トークン上限をチェック

        Args:
            estimated_tokens: 今回使用予定のトークン数

        Returns:
            bool: 上限内かどうか

        Raises:
            TokenLimitExceededError: 上限超過
        """
        try:
            # 今月の総使用量を取得
            current_usage = self.gsheet_client.get_total_tokens_this_month()

            # 新規使用後の総量を計算
            projected_usage = current_usage + estimated_tokens

            # 上限チェック
            if projected_usage > self.monthly_limit:
                raise TokenLimitExceededError(
                    message=f'月次トークン上限を超過します',
                    details={
                        'monthly_limit': self.monthly_limit,
                        'current_usage': current_usage,
                        'estimated_tokens': estimated_tokens,
                        'projected_usage': projected_usage,
                        'remaining': self.monthly_limit - current_usage
                    }
                )

            return True

        except TokenLimitExceededError:
            raise
        except Exception as e:
            # Google Sheets接続エラーなどの場合は警告のみ
            print(f"⚠️  トークン制限チェックエラー: {e}")
            print("⚠️  トークン制限チェックをスキップします")
            return True

    def get_usage_stats(self) -> dict:
        """
        使用量統計を取得

        Returns:
            dict: 統計情報
        """
        try:
            current_usage = self.gsheet_client.get_total_tokens_this_month()

            return {
                'monthly_limit': self.monthly_limit,
                'current_usage': current_usage,
                'remaining': self.monthly_limit - current_usage,
                'usage_percentage': (current_usage / self.monthly_limit * 100) if self.monthly_limit > 0 else 0
            }

        except Exception as e:
            print(f"⚠️  統計取得エラー: {e}")
            return {
                'monthly_limit': self.monthly_limit,
                'current_usage': 0,
                'remaining': self.monthly_limit,
                'usage_percentage': 0,
                'error': str(e)
            }
