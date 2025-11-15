"""
メインアプリケーション
Flaskアプリの初期化とルーティング設定
"""
from flask import Flask
from app.config import get_config
from app.models.errors import register_error_handlers
from app.routes.api_health import health_bp
from app.routes.api_notes import notes_bp
from app.routes.ui_pages import ui_bp


def create_app():
    """Flaskアプリケーションの作成と設定"""
    app = Flask(__name__)

    # 設定読み込み
    config = get_config()
    app.config.from_object(config)

    # 設定の検証
    try:
        config.validate()
    except ValueError as e:
        print(f"⚠️  設定エラー: {e}")
        print("⚠️  開発環境用のデフォルト設定で起動します")

    # エラーハンドラー登録
    register_error_handlers(app)

    # Blueprintの登録
    app.register_blueprint(health_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(ui_bp)

    # アプリケーション起動ログ
    @app.before_request
    def log_request_info():
        """リクエスト情報のログ出力（開発環境のみ）"""
        if app.config.get('DEBUG'):
            from flask import request
            app.logger.debug(f'Request: {request.method} {request.path}')

    return app


# アプリケーションインスタンスの作成
app = create_app()


if __name__ == '__main__':
    # 開発サーバーの起動
    config = get_config()
    print('=' * 70)
    print('🚀 Note記事自動生成システム')
    print('=' * 70)
    print(f'Environment: {config.FLASK_ENV}')
    print(f'Version: {config.VERSION}')
    print(f'Port: {config.PORT}')
    print('=' * 70)
    print()
    print('📋 API エンドポイント:')
    print(f'  - GET  http://localhost:{config.PORT}/api/v1/health')
    print(f'  - POST http://localhost:{config.PORT}/api/v1/notes/generate')
    print(f'  - GET  http://localhost:{config.PORT}/api/v1/notes')
    print()
    print('🖥️  Web UI:')
    print(f'  - http://localhost:{config.PORT}/ （トップ）')
    print(f'  - http://localhost:{config.PORT}/ui/notes/new （新規作成）')
    print(f'  - http://localhost:{config.PORT}/ui/notes （生成履歴）')
    print()
    print('=' * 70)

    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=(config.FLASK_ENV == 'development')
    )
