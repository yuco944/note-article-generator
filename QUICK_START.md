# Renderデプロイ クイックスタート

## 🎯 3ステップでデプロイ

### ステップ1: Renderダッシュボードを開く

1. [https://dashboard.render.com/](https://dashboard.render.com/) を開く
2. ログイン（kindlesyuppan1@gmail.com）

### ステップ2: Webサービスを作成

1. 「New +」→「Web Service」をクリック
2. リポジトリ `yuco944/note-article-generator` を選択
3. 設定を入力（下記参照）
4. 環境変数を設定（`ENV_VARS_CHECKLIST.md` を参照）

### ステップ3: デプロイ実行

1. 「Create Web Service」をクリック
2. 5-10分待つ
3. 完了！

---

## ⚙️ サービス設定（コピー用）

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

---

## 🔑 必須環境変数（3つだけ！）

### 1. LLM_API_KEY
あなたのClaude API Key（`sk-ant-api03-...`）

### 2. GOOGLE_SHEETS_SPREADSHEET_ID
Google SheetsのスプレッドシートID（URLから取得）

### 3. GOOGLE_APPLICATION_CREDENTIALS_JSON
Base64エンコードされたcredentials.json

```bash
cat credentials.json | base64
```

---

## 📚 詳細ガイド

- **完全ガイド**: `RENDER_DEPLOY_STEP_BY_STEP.md` ← これを見ながら進めてください！
- **環境変数チェックリスト**: `ENV_VARS_CHECKLIST.md`
- **環境変数テンプレート**: `render-env-vars.txt`

---

## ✅ デプロイ後の確認

```bash
# ヘルスチェック
curl https://note-article-generator.onrender.com/api/v1/health

# Web UI
open https://note-article-generator.onrender.com/ui/notes/new
```

---

**困ったら `RENDER_DEPLOY_STEP_BY_STEP.md` を開いてください！**

