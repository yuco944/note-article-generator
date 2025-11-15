"""
Google Sheets クライアント
Note_Logsシートへのデータ保存・取得
"""
import os
import json
import base64
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.config import get_config
from app.models.note_models import NoteLogEntry

config = get_config()


class GoogleSheetsClient:
    """Google Sheets API クライアント"""

    def __init__(self):
        """初期化"""
        self.spreadsheet_id = config.GOOGLE_SHEETS_SPREADSHEET_ID
        self.sheet_name = config.GSHEET_NOTE_LOGS_SHEET
        self.service = None
        self._initialize_service()

    def _initialize_service(self):
        """Google Sheets APIサービスの初期化"""
        try:
            credentials = self._get_credentials()
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"⚠️  Google Sheets API初期化エラー: {e}")
            print("⚠️  Google Sheets機能は無効化されます")
            self.service = None

    def _get_credentials(self):
        """認証情報の取得"""
        # スコープの定義
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # 本番環境: 環境変数からJSON取得
        if config.GOOGLE_APPLICATION_CREDENTIALS_JSON:
            try:
                credentials_json = base64.b64decode(
                    config.GOOGLE_APPLICATION_CREDENTIALS_JSON
                ).decode('utf-8')
                credentials_dict = json.loads(credentials_json)
                return service_account.Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=SCOPES
                )
            except Exception as e:
                print(f"⚠️  環境変数からの認証情報読み込みエラー: {e}")

        # 開発環境: credentials.jsonファイルから取得
        credentials_file = config.GOOGLE_APPLICATION_CREDENTIALS
        if os.path.exists(credentials_file):
            return service_account.Credentials.from_service_account_file(
                credentials_file,
                scopes=SCOPES
            )

        raise ValueError('Google認証情報が見つかりません')

    def append_row(self, log_entry: NoteLogEntry) -> bool:
        """
        Note_Logsシートに行を追加

        Args:
            log_entry: ログエントリ

        Returns:
            bool: 成功/失敗
        """
        if not self.service:
            print("⚠️  Google Sheets サービスが初期化されていません")
            return False

        try:
            # ヘッダー行の確認・作成
            self._ensure_header_row()

            # データ行の追加
            range_name = f'{self.sheet_name}!A:L'
            values = [log_entry.to_row()]

            body = {
                'values': values
            }

            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            print(f"✅ Google Sheets に保存: {log_entry.note_id}")
            return True

        except HttpError as e:
            print(f"❌ Google Sheets エラー: {e}")
            return False
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            return False

    def _ensure_header_row(self):
        """ヘッダー行の確認・作成"""
        try:
            # シートの最初の行を取得
            range_name = f'{self.sheet_name}!A1:L1'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])

            # ヘッダー行が存在しない場合は作成
            if not values:
                header_row = NoteLogEntry.get_header_row()
                body = {
                    'values': [header_row]
                }

                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='RAW',
                    body=body
                ).execute()

                print("✅ ヘッダー行を作成しました")

        except Exception as e:
            print(f"⚠️  ヘッダー行の確認エラー: {e}")

    def get_recent_logs(self, limit: int = 20) -> List[Dict]:
        """
        最新のログを取得

        Args:
            limit: 取得件数

        Returns:
            List[Dict]: ログデータ
        """
        if not self.service:
            print("⚠️  Google Sheets サービスが初期化されていません")
            return []

        try:
            # シート全体を取得
            range_name = f'{self.sheet_name}!A:L'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])

            if len(values) <= 1:
                # ヘッダー行のみ、またはデータなし
                return []

            # ヘッダー行を除外
            header = values[0]
            data_rows = values[1:]

            # 最新limit件を取得（逆順）
            recent_rows = data_rows[-limit:][::-1]

            # 辞書形式に変換
            logs = []
            for row in recent_rows:
                # 行の長さが足りない場合は空文字で埋める
                while len(row) < len(header):
                    row.append('')

                log_dict = {
                    'note_id': row[0] if len(row) > 0 else '',
                    'topic': row[1] if len(row) > 1 else '',
                    'title': row[8] if len(row) > 8 else '',
                    'created_at': row[11] if len(row) > 11 else '',
                    'article_type': row[4] if len(row) > 4 else '',
                    'intensity_level': int(row[7]) if len(row) > 7 and row[7] else 0,
                    'total_tokens': int(row[10]) if len(row) > 10 and row[10] else 0
                }
                logs.append(log_dict)

            return logs

        except HttpError as e:
            print(f"❌ Google Sheets エラー: {e}")
            return []
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            return []

    def get_total_tokens_this_month(self) -> int:
        """
        今月の総トークン使用量を取得

        Returns:
            int: 総トークン数
        """
        if not self.service:
            return 0

        try:
            from datetime import datetime

            # 今月の開始日
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_start_str = month_start.isoformat()

            # 全データ取得
            range_name = f'{self.sheet_name}!A:L'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])

            if len(values) <= 1:
                return 0

            # ヘッダー行を除外
            data_rows = values[1:]

            # 今月のデータのみ集計
            total_tokens = 0
            for row in data_rows:
                if len(row) < 12:
                    continue

                created_at = row[11]  # created_at列
                total_tokens_str = row[10]  # total_tokens列

                try:
                    # 日付比較
                    if created_at >= month_start_str:
                        total_tokens += int(total_tokens_str)
                except (ValueError, TypeError):
                    continue

            return total_tokens

        except Exception as e:
            print(f"⚠️  トークン集計エラー: {e}")
            return 0


# シングルトンインスタンス
_gsheet_client_instance: Optional[GoogleSheetsClient] = None


def get_gsheet_client() -> GoogleSheetsClient:
    """Google Sheets クライアントのシングルトンインスタンスを取得"""
    global _gsheet_client_instance
    if _gsheet_client_instance is None:
        _gsheet_client_instance = GoogleSheetsClient()
    return _gsheet_client_instance
