# Renderデプロイガイド

## ✅ 完了したステップ

1. ✅ Render CLIのインストール
2. ✅ Render CLIでの認証（kindlesyuppan1@gmail.com）
3. ✅ GitHubリポジトリへのプッシュ
4. ✅ デプロイ自動化スクリプトの作成

## 📋 次のステップ：RenderダッシュボードでWebサービスを作成

### ステップ1: Renderダッシュボードにアクセス

1. ブラウザで [Render Dashboard](https://dashboard.render.com/) にアクセス
2. ログイン（kindlesyuppan1@gmail.com）

### ステップ2: 新しいWebサービスを作成

1. ダッシュボードで「**New +**」ボタンをクリック
2. 「**Web Service**」を選択
3. GitHubリポジトリを接続（初回の場合）:
   - 「**Connect account**」をクリックしてGitHubアカウントを接続
   - リポジトリ `yuco944/note-article-generator` を選択

### ステップ3: サービス設定

以下の設定を入力：

- **Name**: `note-article-generator`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Root Directory**: （空白のまま）
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.main:app --bind 0.0.0.0:$PORT`
- **Plan**: `Free`（無料プラン）

### ステップ4: 環境変数の設定

「**Environment Variables**」セクションで以下を設定：

#### 必須環境変数

```bash
# Flask設定
FLASK_ENV=production
PORT=10000

# LLM設定
LLM_PROVIDER=claude
LLM_API_KEY=sk-ant-...（あなたのClaude API Key）
LLM_MODEL_AGENT1=claude-3-5-sonnet-20241022
LLM_MODEL_AGENT2=claude-3-5-sonnet-20241022
LLM_AGENT1_MAX_TOKENS=6000
LLM_AGENT2_MAX_TOKENS=4000

# Google Sheets設定
GOOGLE_SHEETS_SPREADSHEET_ID=あなたのスプレッドシートID
GSHEET_NOTE_LOGS_SHEET=Note_Logs
GOOGLE_APPLICATION_CREDENTIALS_JSON=（Base64エンコードされたcredentials.jsonの内容）

# アプリケーション設定
ADMIN_API_KEY=（ランダムな文字列、例：openssl rand -hex 32で生成）
MONTHLY_TOKEN_LIMIT=300000
```

#### 環境変数の準備方法

以下のスクリプトを実行して環境変数を準備できます：

```bash
./scripts/setup-render-env.sh
```

このスクリプトは `render-env-vars.txt` ファイルを生成します。その内容をRenderダッシュボードにコピー＆ペーストしてください。

### ステップ5: デプロイ実行

1. 「**Create Web Service**」ボタンをクリック
2. デプロイが開始されます（数分かかります）
3. デプロイ完了後、URLが表示されます（例：`https://note-article-generator.onrender.com`）

### ステップ6: 動作確認

デプロイ完了後、以下で動作確認：

```bash
# ヘルスチェック
curl https://note-article-generator.onrender.com/api/v1/health

# Web UI確認
open https://note-article-generator.onrender.com/ui/notes/new
```

## 🔧 トラブルシューティング

### ビルドエラー

- `requirements.txt` の内容を確認
- Pythonバージョンを確認（`runtime.txt`で指定可能）

### 起動エラー

- Render Dashboard → Logs でログを確認
- 環境変数が正しく設定されているか確認

### Google Sheets接続エラー

- `GOOGLE_SHEETS_SPREADSHEET_ID` が正しいか確認
- サービスアカウントに編集権限があるか確認
- `GOOGLE_APPLICATION_CREDENTIALS_JSON` が正しくBase64エンコードされているか確認

## 📝 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [デプロイ手順詳細](./docs/deploy.md)
- [スクリプトの使い方](./scripts/README.md)

