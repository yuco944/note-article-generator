# Renderデプロイ完全ガイド（ステップバイステップ）

このガイドでは、Renderダッシュボードでの操作を画面ごとに詳しく説明します。

---

## 📋 事前準備チェックリスト

デプロイを始める前に、以下を準備してください：

- [ ] Claude API Key（`sk-ant-api03-...` で始まる文字列）
- [ ] Google SheetsのスプレッドシートID
- [ ] Google認証情報ファイル（`credentials.json`）

---

## 🚀 ステップ1: Renderダッシュボードにアクセス

### 1-1. ブラウザでダッシュボードを開く

1. ブラウザで以下のURLを開きます：
   ```
   https://dashboard.render.com/
   ```

2. ログイン画面が表示されたら、以下でログイン：
   - **Email**: `kindlesyuppan1@gmail.com`
   - **Password**: （あなたのパスワード）

3. ログイン後、ダッシュボードのトップページが表示されます

---

## 🚀 ステップ2: 新しいWebサービスを作成

### 2-1. 「New +」ボタンをクリック

1. ダッシュボードの左上または右上にある **「New +」** ボタンを探します
2. **「New +」** ボタンをクリックします
3. ドロップダウンメニューが表示されます

### 2-2. 「Web Service」を選択

1. ドロップダウンメニューから **「Web Service」** を選択します
2. 新しいページ（サービス作成画面）に遷移します

---

## 🚀 ステップ3: GitHubリポジトリを接続

### 3-1. GitHubアカウントの接続（初回のみ）

**もしGitHubアカウントがまだ接続されていない場合：**

1. 「Connect a repository」セクションで **「Connect account」** または **「Connect GitHub」** ボタンをクリック
2. GitHubの認証画面が表示されます
3. 「Authorize Render」をクリックして許可します
4. Renderダッシュボードに戻ります

### 3-2. リポジトリを選択

1. 「Repository」セクションで、リポジトリ一覧が表示されます
2. 検索ボックスに `note-article-generator` と入力
3. **`yuco944/note-article-generator`** を選択します
4. 選択後、リポジトリ情報が表示されます

---

## 🚀 ステップ4: サービス設定を入力

以下の各項目を、画面の指示に従って入力してください。

### 4-1. 基本設定

| 項目 | 入力値 | 説明 |
|------|--------|------|
| **Name** | `note-article-generator` | サービスの名前（任意の名前でも可） |
| **Region** | `Oregon (US West)` | サーバーの場所（無料プランはOregonのみ） |
| **Branch** | `main` | デプロイするGitブランチ |
| **Root Directory** | （空白のまま） | プロジェクトのルートディレクトリ |

### 4-2. ビルド・起動設定

| 項目 | 入力値 | 説明 |
|------|--------|------|
| **Environment** | `Python 3` | 実行環境（ドロップダウンから選択） |
| **Build Command** | `pip install -r requirements.txt` | 依存パッケージのインストールコマンド |
| **Start Command** | `gunicorn app.main:app --bind 0.0.0.0:$PORT` | アプリケーション起動コマンド |

### 4-3. プラン選択

1. 「Plan」セクションで **「Free」** を選択します
   - 無料プランは自動スリープする場合があります

---

## 🚀 ステップ5: 環境変数を設定

このステップが最も重要です。環境変数を正しく設定しないと、アプリケーションが動作しません。

### 5-1. 環境変数セクションを開く

1. 画面を下にスクロールします
2. **「Environment Variables」** セクションを見つけます
3. 「Add Environment Variable」ボタンまたは「+」ボタンをクリック

### 5-2. 環境変数を1つずつ追加

以下の環境変数を、**1つずつ**追加してください。

#### ✅ 環境変数1: FLASK_ENV

1. 「Key」欄に `FLASK_ENV` と入力
2. 「Value」欄に `production` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数2: PORT

1. 「Key」欄に `PORT` と入力
2. 「Value」欄に `10000` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数3: LLM_PROVIDER

1. 「Key」欄に `LLM_PROVIDER` と入力
2. 「Value」欄に `claude` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数4: LLM_API_KEY（重要！）

1. 「Key」欄に `LLM_API_KEY` と入力
2. 「Value」欄に、あなたのClaude API Keyを貼り付け
   - 例: `sk-ant-api03-xxxxxxxxxxxxx...`
   - **注意**: この値は機密情報です。他人に見せないでください
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数5: LLM_MODEL_AGENT1

1. 「Key」欄に `LLM_MODEL_AGENT1` と入力
2. 「Value」欄に `claude-3-5-sonnet-20241022` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数6: LLM_MODEL_AGENT2

1. 「Key」欄に `LLM_MODEL_AGENT2` と入力
2. 「Value」欄に `claude-3-5-sonnet-20241022` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数7: LLM_AGENT1_MAX_TOKENS

1. 「Key」欄に `LLM_AGENT1_MAX_TOKENS` と入力
2. 「Value」欄に `6000` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数8: LLM_AGENT2_MAX_TOKENS

1. 「Key」欄に `LLM_AGENT2_MAX_TOKENS` と入力
2. 「Value」欄に `4000` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数9: MONTHLY_TOKEN_LIMIT

1. 「Key」欄に `MONTHLY_TOKEN_LIMIT` と入力
2. 「Value」欄に `300000` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数10: GOOGLE_SHEETS_SPREADSHEET_ID（重要！）

1. 「Key」欄に `GOOGLE_SHEETS_SPREADSHEET_ID` と入力
2. 「Value」欄に、Google SheetsのスプレッドシートIDを入力
   - スプレッドシートのURLから取得:
     ```
     https://docs.google.com/spreadsheets/d/{ここがスプレッドシートID}/edit
     ```
   - 例: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数11: GSHEET_NOTE_LOGS_SHEET

1. 「Key」欄に `GSHEET_NOTE_LOGS_SHEET` と入力
2. 「Value」欄に `Note_Logs` と入力
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数12: GOOGLE_APPLICATION_CREDENTIALS_JSON（重要！）

この環境変数は、Google認証情報をBase64エンコードしたものです。

**事前準備（ターミナルで実行）:**

```bash
cd /Users/yuco/div/note/note-article-generator
cat credentials.json | base64
```

このコマンドを実行すると、長い文字列が表示されます。**この文字列全体をコピー**してください。

**Renderダッシュボードで設定:**

1. 「Key」欄に `GOOGLE_APPLICATION_CREDENTIALS_JSON` と入力
2. 「Value」欄に、コピーしたBase64文字列を貼り付け
   - **注意**: 非常に長い文字列です。全体をコピーしてください
3. 「Add」または「Save」ボタンをクリック

#### ✅ 環境変数13: ADMIN_API_KEY

1. 「Key」欄に `ADMIN_API_KEY` と入力
2. 「Value」欄に `17982538f8945934fa629324eaf86bf92cacab5e4e388ed8c74210457d7d1372` と入力
   - （これは既に生成済みの値です）
3. 「Add」または「Save」ボタンをクリック

### 5-3. 環境変数の確認

すべての環境変数を追加したら、一覧を確認してください：

- [ ] FLASK_ENV = production
- [ ] PORT = 10000
- [ ] LLM_PROVIDER = claude
- [ ] LLM_API_KEY = （あなたのAPI Key）
- [ ] LLM_MODEL_AGENT1 = claude-3-5-sonnet-20241022
- [ ] LLM_MODEL_AGENT2 = claude-3-5-sonnet-20241022
- [ ] LLM_AGENT1_MAX_TOKENS = 6000
- [ ] LLM_AGENT2_MAX_TOKENS = 4000
- [ ] MONTHLY_TOKEN_LIMIT = 300000
- [ ] GOOGLE_SHEETS_SPREADSHEET_ID = （あなたのスプレッドシートID）
- [ ] GSHEET_NOTE_LOGS_SHEET = Note_Logs
- [ ] GOOGLE_APPLICATION_CREDENTIALS_JSON = （Base64文字列）
- [ ] ADMIN_API_KEY = 17982538f8945934fa629324eaf86bf92cacab5e4e388ed8c74210457d7d1372

---

## 🚀 ステップ6: デプロイを開始

### 6-1. 「Create Web Service」ボタンをクリック

1. 画面を下にスクロールします
2. 画面下部にある **「Create Web Service」** ボタンをクリックします
3. デプロイが開始されます

### 6-2. デプロイの進行を確認

1. デプロイ画面に遷移します
2. 「Build Log」タブで、ビルドの進行状況を確認できます
3. 以下のようなログが表示されます：
   ```
   ==> Cloning from https://github.com/yuco944/note-article-generator.git
   ==> Building...
   ==> Installing dependencies...
   ==> Starting service...
   ```

### 6-3. デプロイ完了を待つ

- デプロイには **5-10分程度** かかります
- 「Live」という緑色のバッジが表示されたら、デプロイ完了です
- サービスのURLが表示されます（例: `https://note-article-generator.onrender.com`）

---

## 🚀 ステップ7: 動作確認

### 7-1. ヘルスチェック

ターミナルで以下を実行：

```bash
curl https://note-article-generator.onrender.com/api/v1/health
```

**期待されるレスポンス:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### 7-2. Web UIの確認

ブラウザで以下を開きます：

```
https://note-article-generator.onrender.com/ui/notes/new
```

記事生成フォームが表示されれば成功です！

---

## ❌ トラブルシューティング

### ビルドエラーが発生した場合

1. Renderダッシュボードの「Logs」タブを確認
2. エラーメッセージを確認
3. よくある原因：
   - `requirements.txt` の依存パッケージエラー
   - Pythonバージョンの不一致

### 起動エラーが発生した場合

1. 「Logs」タブでエラーログを確認
2. 環境変数が正しく設定されているか確認
3. よくある原因：
   - `LLM_API_KEY` が設定されていない
   - `GOOGLE_APPLICATION_CREDENTIALS_JSON` が正しくエンコードされていない

### サービスが起動しない場合

1. 環境変数を再確認
2. 「Events」タブでイベントログを確認
3. 必要に応じてサービスを再起動（「Manual Deploy」→「Clear build cache & deploy」）

---

## 📝 参考情報

- **環境変数テンプレート**: `render-env-vars.txt`
- **デプロイガイド**: `DEPLOYMENT_GUIDE.md`
- **次のステップ**: `NEXT_STEPS.md`

---

## 💡 ヒント

- 環境変数は後からでも追加・編集できます
- デプロイ後も設定を変更できます（「Environment」タブから）
- 無料プランは15分間アクセスがないと自動スリープします（次回アクセス時に自動起動）

---

**質問があれば、いつでもお聞きください！**

