"""
UI ページルーティング
記事生成フォームと履歴表示
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.note_service import NoteService
from app.models.errors import ValidationError, TokenLimitExceededError

ui_bp = Blueprint('ui', __name__)
note_service = NoteService()


@ui_bp.route('/ui/notes/new', methods=['GET'])
def notes_new():
    """記事生成フォーム"""
    return render_template('notes_new.html')


@ui_bp.route('/ui/notes/new', methods=['POST'])
def notes_create():
    """記事生成実行"""
    try:
        # フォームデータ取得
        request_data = {
            'topic': request.form.get('topic', ''),
            'audience': request.form.get('audience', ''),
            'goal': request.form.get('goal', ''),
            'article_type': request.form.get('article_type', 'education'),
            'length_class': request.form.get('length_class', 'middle'),
            'temperature': float(request.form.get('temperature', 0.7)),
            'intensity_level': int(request.form.get('intensity_level', 5))
        }

        # 記事生成
        response = note_service.generate_note(request_data)

        # 成功時は結果表示ページへ
        return render_template('notes_result.html', result=response)

    except ValidationError as e:
        flash(f'入力エラー: {e.message}', 'error')
        return render_template('notes_new.html', form_data=request.form)

    except TokenLimitExceededError as e:
        flash(f'トークン上限エラー: {e.message}', 'error')
        flash(f'残りトークン: {e.details.get("remaining", 0)}', 'info')
        return render_template('notes_new.html', form_data=request.form)

    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
        return render_template('notes_new.html', form_data=request.form)


@ui_bp.route('/ui/notes', methods=['GET'])
def notes_index():
    """記事履歴一覧"""
    try:
        # Google Sheetsから最新20件取得
        from app.clients.gsheet_client import get_gsheet_client
        gsheet_client = get_gsheet_client()
        logs = gsheet_client.get_recent_logs(limit=20)

        return render_template('notes_index.html', logs=logs)

    except Exception as e:
        flash(f'履歴取得エラー: {str(e)}', 'error')
        return render_template('notes_index.html', logs=[])


@ui_bp.route('/ui', methods=['GET'])
@ui_bp.route('/', methods=['GET'])
def index():
    """トップページ - 新規作成ページへリダイレクト"""
    return redirect(url_for('ui.notes_new'))
