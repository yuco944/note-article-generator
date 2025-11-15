"""
ヘルスチェックAPI
アプリケーションの稼働状況を確認するエンドポイント
"""
from flask import Blueprint, jsonify
from app.config import get_config

# Blueprintの作成
health_bp = Blueprint('health', __name__)

config = get_config()


@health_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    ヘルスチェック

    Returns:
        JSON: ステータスとバージョン情報
    """
    return jsonify({
        'status': 'ok',
        'version': config.VERSION
    }), 200
