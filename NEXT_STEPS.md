# 次のステップ：Renderデプロイ

## ✅ 完了したこと

1. ✅ Render CLIのインストール
2. ✅ Render CLIでの認証
3. ✅ デプロイスクリプトの作成
4. ✅ 環境変数ファイルの生成（`render-env-vars.txt`）

## 📋 今すぐ実行する手順

### ステップ1: RenderダッシュボードでWebサービスを作成

1. **ブラウザで [Render Dashboard](https://dashboard.render.com/) を開く**
   - 既にログイン済み（kindlesyuppan1@gmail.com）

2. **「New +」ボタンをクリック → 「Web Service」を選択**

3. **GitHubリポジトリを接続**
   - リポジトリ: `yuco944/note-article-generator`
   - ブランチ: `main`

4. **サービス設定を入力**
   ```
   Name: note-article-generator
   Region: Oregon (US West)
   Branch: main
   Root Directory: （空白）
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app.main:app --bind 0.0.0.0:$PORT
   Plan: Free
   ```

### ステップ2: 環境変数を設定

「Environment Variables」セクションで、`render-env-vars.txt`の内容を設定します。

**必須の環境変数（設定が必要）:**

1. **LLM_API_KEY**: あなたのClaude API Key
   - 例: `sk-ant-api03-...`

2. **GOOGLE_SHEETS_SPREADSHEET_ID**: Google SheetsのスプレッドシートID
   - スプレッドシートのURLから取得: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

3. **GOOGLE_APPLICATION_CREDENTIALS_JSON**: Base64エンコードされたcredentials.json
   - 以下のコマンドで生成:
   ```bash
   cat credentials.json | base64
   ```
   - 出力された文字列全体をコピーして設定

**既に設定済み（そのまま使用）:**
- `ADMIN_API_KEY`（自動生成済み）
- その他の環境変数（`render-env-vars.txt`を参照）

### ステップ3: デプロイ実行

1. 「**Create Web Service**」ボタンをクリック
2. デプロイが開始されます（5-10分程度）
3. デプロイ完了後、URLが表示されます

### ステップ4: 動作確認

デプロイ完了後、以下で確認:

```bash
# ヘルスチェック
curl https://note-article-generator.onrender.com/api/v1/health

# Web UI
open https://note-article-generator.onrender.com/ui/notes/new
```

## 🔧 環境変数の準備（オプション）

もし環境変数を再度準備する場合:

```bash
./scripts/setup-render-env.sh
```

## 📝 参考

- 詳細ガイド: `DEPLOYMENT_GUIDE.md`
- 環境変数ファイル: `render-env-vars.txt`
- デプロイスクリプト: `scripts/deploy-to-render.sh`

