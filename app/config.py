"""
アプリケーション設定
環境変数から設定を読み込む
"""
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


class Config:
    """アプリケーション設定クラス"""

    # Flask設定
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 8000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # LLM設定
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'claude')  # claude_or_openai
    LLM_API_KEY = os.getenv('LLM_API_KEY')
    LLM_MODEL_AGENT1 = os.getenv('LLM_MODEL_AGENT1', 'claude-3-5-sonnet-20241022')
    LLM_MODEL_AGENT2 = os.getenv('LLM_MODEL_AGENT2', 'claude-3-5-sonnet-20241022')
    LLM_AGENT1_MAX_TOKENS = int(os.getenv('LLM_AGENT1_MAX_TOKENS', 6000))
    LLM_AGENT2_MAX_TOKENS = int(os.getenv('LLM_AGENT2_MAX_TOKENS', 4000))

    # Google Sheets設定
    GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    GSHEET_NOTE_LOGS_SHEET = os.getenv('GSHEET_NOTE_LOGS_SHEET', 'Note_Logs')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
    GOOGLE_APPLICATION_CREDENTIALS_JSON = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')  # Base64エンコードされたJSON

    # アプリケーション設定
    ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'change_me')
    MONTHLY_TOKEN_LIMIT = int(os.getenv('MONTHLY_TOKEN_LIMIT', 300000))

    # バージョン
    VERSION = '1.0.0'

    @classmethod
    def validate(cls):
        """必須の環境変数が設定されているか検証"""
        required_vars = [
            ('LLM_API_KEY', cls.LLM_API_KEY),
        ]

        missing = [var_name for var_name, var_value in required_vars if not var_value]

        if missing:
            raise ValueError(f"必須の環境変数が設定されていません: {', '.join(missing)}")

        return True


# 開発環境用のデフォルト設定
class DevelopmentConfig(Config):
    """開発環境用設定"""
    DEBUG = True


# 本番環境用の設定
class ProductionConfig(Config):
    """本番環境用設定"""
    DEBUG = False


# 環境に応じた設定を選択
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config():
    """現在の環境に応じた設定を取得"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
