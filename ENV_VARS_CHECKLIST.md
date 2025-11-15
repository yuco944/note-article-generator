# 環境変数設定チェックリスト

Renderダッシュボードで環境変数を設定する際に、このチェックリストを使用してください。

## 📋 環境変数一覧（コピー用）

以下の環境変数を、Renderダッシュボードの「Environment Variables」セクションで1つずつ追加してください。

---

### ✅ 1. FLASK_ENV

```
Key: FLASK_ENV
Value: production
```

---

### ✅ 2. PORT

```
Key: PORT
Value: 10000
```

---

### ✅ 3. LLM_PROVIDER

```
Key: LLM_PROVIDER
Value: claude
```

---

### ✅ 4. LLM_API_KEY ⚠️ 重要

```
Key: LLM_API_KEY
Value: （あなたのClaude API Keyをここに入力）
```

**取得方法:**
- Anthropicのダッシュボードから取得
- `sk-ant-api03-...` で始まる文字列

---

### ✅ 5. LLM_MODEL_AGENT1

```
Key: LLM_MODEL_AGENT1
Value: claude-3-5-sonnet-20241022
```

---

### ✅ 6. LLM_MODEL_AGENT2

```
Key: LLM_MODEL_AGENT2
Value: claude-3-5-sonnet-20241022
```

---

### ✅ 7. LLM_AGENT1_MAX_TOKENS

```
Key: LLM_AGENT1_MAX_TOKENS
Value: 6000
```

---

### ✅ 8. LLM_AGENT2_MAX_TOKENS

```
Key: LLM_AGENT2_MAX_TOKENS
Value: 4000
```

---

### ✅ 9. MONTHLY_TOKEN_LIMIT

```
Key: MONTHLY_TOKEN_LIMIT
Value: 300000
```

---

### ✅ 10. GOOGLE_SHEETS_SPREADSHEET_ID ⚠️ 重要

```
Key: GOOGLE_SHEETS_SPREADSHEET_ID
Value: （あなたのスプレッドシートIDをここに入力）
```

**取得方法:**
1. Google Sheetsを開く
2. URLを確認: `https://docs.google.com/spreadsheets/d/{ここがID}/edit`
3. `{ここがID}` の部分をコピー

**例:**
```
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t/edit
```
→ スプレッドシートIDは `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

---

### ✅ 11. GSHEET_NOTE_LOGS_SHEET

```
Key: GSHEET_NOTE_LOGS_SHEET
Value: Note_Logs
```

**注意:** スプレッドシート内に「Note_Logs」という名前のシートが必要です。

---

### ✅ 12. GOOGLE_APPLICATION_CREDENTIALS_JSON ⚠️ 重要

```
Key: GOOGLE_APPLICATION_CREDENTIALS_JSON
Value: （Base64エンコードされた文字列をここに入力）
```

**準備方法:**

1. ターミナルを開く
2. 以下のコマンドを実行:

```bash
cd /Users/yuco/div/note/note-article-generator
cat credentials.json | base64
```

3. 表示された長い文字列全体をコピー
4. Renderダッシュボードの「Value」欄に貼り付け

**注意:**
- 文字列は非常に長いです（数千文字）
- 全体をコピーしてください
- 改行は含めないでください

---

### ✅ 13. ADMIN_API_KEY

```
Key: ADMIN_API_KEY
Value: 17982538f8945934fa629324eaf86bf92cacab5e4e388ed8c74210457d7d1372
```

**注意:** この値は既に生成済みです。そのまま使用してください。

---

## ✅ 設定完了チェックリスト

すべての環境変数を追加したら、以下を確認してください：

- [ ] FLASK_ENV = production
- [ ] PORT = 10000
- [ ] LLM_PROVIDER = claude
- [ ] LLM_API_KEY = （あなたのAPI Key）✅
- [ ] LLM_MODEL_AGENT1 = claude-3-5-sonnet-20241022
- [ ] LLM_MODEL_AGENT2 = claude-3-5-sonnet-20241022
- [ ] LLM_AGENT1_MAX_TOKENS = 6000
- [ ] LLM_AGENT2_MAX_TOKENS = 4000
- [ ] MONTHLY_TOKEN_LIMIT = 300000
- [ ] GOOGLE_SHEETS_SPREADSHEET_ID = （あなたのスプレッドシートID）✅
- [ ] GSHEET_NOTE_LOGS_SHEET = Note_Logs
- [ ] GOOGLE_APPLICATION_CREDENTIALS_JSON = （Base64文字列）✅
- [ ] ADMIN_API_KEY = 17982538f8945934fa629324eaf86bf92cacab5e4e388ed8c74210457d7d1372

---

## 💡 ヒント

- 環境変数は後からでも追加・編集できます
- 設定後は「Save Changes」をクリックしてください
- 環境変数を削除する場合は、各変数の右側にある「×」ボタンをクリック

---

## 📝 参考

- 詳細な手順: `RENDER_DEPLOY_STEP_BY_STEP.md`
- 環境変数テンプレート: `render-env-vars.txt`

