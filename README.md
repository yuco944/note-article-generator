# Note記事自動生成システム

SNS用note記事の叩き台（タイトル〜本文〜CTA）を自動生成するWebアプリ＆APIシステム。

## 機能

- **記事自動生成**: テーマ・読者・温度・煽り度などのパラメータから記事を自動生成
- **Google Sheets連携**: 生成ログを自動保存
- **トークン制限**: 月次トークン使用量の管理
- **Web UI**: ブラウザから簡単に記事生成
- **REST API**: プログラムからの呼び出しに対応

## 技術スタック

- **Backend**: Python 3.x + Flask
- **LLM**: Claude / OpenAI (環境変数で切り替え可能)
- **Database**: Google Sheets API
- **Server**: Gunicorn (本番環境)

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.sample` をコピーして `.env` を作成し、必要な値を設定してください。

```bash
cp .env.sample .env
```

必須の環境変数:
- `LLM_API_KEY`: Claude または OpenAI の APIキー
- `GOOGLE_SHEETS_SPREADSHEET_ID`: Google Sheets のスプレッドシートID
- `ADMIN_API_KEY`: 管理用APIキー（ランダムな文字列を設定）

### 3. Google Sheets の準備

1. Google Cloud Console で プロジェクトを作成
2. Google Sheets API を有効化
3. サービスアカウントを作成して `credentials.json` をダウンロード
4. スプレッドシートを作成し、サービスアカウントに編集権限を付与
5. `Note_Logs` という名前のシートを作成

**Note_Logs シートの列構成:**
```
note_id | topic | audience | goal | article_type | length_class | temperature | intensity_level | title | raw_json | total_tokens | created_at
```

### 4. アプリケーションの起動

**開発環境:**
```bash
python -m flask --app app.main run --port 8000
```

**本番環境:**
```bash
gunicorn app.main:app --bind 0.0.0.0:$PORT
```

## API エンドポイント

### POST /api/v1/notes/generate

記事を自動生成します。

**リクエスト:**
```json
{
  "topic": "月100万の壁を超えられない",
  "audience": "情報発信で月30〜70万で伸び悩む人",
  "goal": "構造の重要性を教育する",
  "article_type": "education",
  "length_class": "middle",
  "temperature": 0.8,
  "intensity_level": 7
}
```

**レスポンス:**
```json
{
  "status": "SUCCESS",
  "note_id": "note_20251115_0001",
  "title": "...",
  "lead": "...",
  "sections": [
    { "heading": "見出し1", "body": "本文テキスト..." }
  ],
  "cta": "...行動喚起テキスト...",
  "metadata": { ... }
}
```

### GET /api/v1/notes

生成履歴を取得します。

### GET /api/v1/health

ヘルスチェック用エンドポイント。

## Web UI

- `/ui/notes/new`: 記事生成フォーム
- `/ui/notes`: 生成履歴一覧

## テスト

```bash
pytest tests/
```

## デプロイ

### クイックスタート（自動化スクリプト使用）

Renderへのデプロイを自動化するスクリプトを用意しています：

```bash
# 1. 環境変数の設定支援
./scripts/setup-render-env.sh

# 2. Renderへのデプロイ実行
./scripts/deploy-to-render.sh
```

### 手動デプロイ

詳細は `docs/deploy.md` を参照してください。

## ライセンス

MIT License

## 作成者

トミー式ナレッジ実装チーム
