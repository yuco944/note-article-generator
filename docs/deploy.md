# デプロイ手順

## Renderへのデプロイ

### 🚀 クイックスタート（自動化スクリプト）

デプロイを簡単にするための自動化スクリプトを用意しています。

#### ステップ1: 環境変数の準備

```bash
./scripts/setup-render-env.sh
```

このスクリプトは以下を行います：
- 必要な環境変数の入力支援
- Google認証情報のBase64エンコード
- 環境変数設定ファイルの生成
- Render CLIを使用した環境変数の自動設定（オプション）

#### ステップ2: Renderへのデプロイ

```bash
./scripts/deploy-to-render.sh
```

このスクリプトは以下を行います：
- Render CLIのインストール確認・インストール
- Render認証の確認
- 必須環境変数の確認
- Gitリポジトリの確認・初期化
- Renderサービスの作成/更新

**注意**: 初回デプロイの場合は、GitHubリポジトリを事前に作成し、RenderダッシュボードでWebサービスを作成する必要があります。

---

### 📝 手動デプロイ手順

自動化スクリプトを使用しない場合は、以下の手順に従ってください。

#### 1. GitHubにプッシュ

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/note-article-generator.git
git push -u origin main
```

### 2. Renderで「New Web Service」を作成

1. [Render Dashboard](https://dashboard.render.com/) にアクセス
2. 「New +」→「Web Service」を選択
3. GitHubリポジトリを選択

### 3. ビルド設定

- **Name**: `note-article-generator`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.main:app --bind 0.0.0.0:$PORT`

### 4. 環境変数の設定

Renderの環境変数画面で以下を登録:

```
FLASK_ENV=production
PORT=10000

LLM_PROVIDER=claude
LLM_API_KEY=sk-ant-...
LLM_MODEL_AGENT1=claude-3-5-sonnet-20241022
LLM_MODEL_AGENT2=claude-3-5-sonnet-20241022
LLM_AGENT1_MAX_TOKENS=6000
LLM_AGENT2_MAX_TOKENS=4000

GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GSHEET_NOTE_LOGS_SHEET=Note_Logs

ADMIN_API_KEY=your_random_string_here
MONTHLY_TOKEN_LIMIT=300000
```

### 5. Google認証情報の設定（本番環境）

#### オプション1: 環境変数経由（推奨）

credentials.jsonの内容をbase64エンコード:

```bash
cat credentials.json | base64
```

Renderの環境変数に追加:

```
GOOGLE_APPLICATION_CREDENTIALS_JSON=<base64エンコードされた内容>
```

#### オプション2: ファイル経由

Renderのディスク機能を使用してcredentials.jsonをアップロード

### 6. デプロイ実行

「Create Web Service」ボタンをクリック

### 7. 動作確認

デプロイ完了後、以下をチェック:

#### ヘルスチェック

```bash
curl https://note-article-generator.onrender.com/api/v1/health
```

期待されるレスポンス:

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### UI確認

ブラウザで以下にアクセス:

```
https://note-article-generator.onrender.com/ui/notes/new
```

#### API確認

```bash
curl -X POST https://note-article-generator.onrender.com/api/v1/notes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "テスト記事",
    "audience": "一般読者",
    "goal": "情報提供",
    "article_type": "education",
    "length_class": "short",
    "temperature": 0.7,
    "intensity_level": 5
  }'
```

## トラブルシューティング

### ビルドエラー

- `requirements.txt` の内容を確認
- Python バージョンを確認 (runtime.txt で指定可能)

### 起動エラー

- ログを確認: Render Dashboard → Logs
- 環境変数が正しく設定されているか確認

### Google Sheets接続エラー

- `GOOGLE_SHEETS_SPREADSHEET_ID` が正しいか確認
- サービスアカウントに編集権限があるか確認
- credentials.json が正しく読み込まれているか確認

## ローカルテスト

本番環境と同じ設定でローカルテストする:

```bash
export FLASK_ENV=production
gunicorn app.main:app --bind 0.0.0.0:8000
```

## 環境別設定

### 開発環境

```bash
FLASK_ENV=development
```

- デバッグモード有効
- 詳細なエラーメッセージ表示

### 本番環境

```bash
FLASK_ENV=production
```

- デバッグモード無効
- エラーメッセージは最小限
