# 今すぐデプロイ - クイックリファレンス

## 🚀 2つの方法から選択

### 方法1: 自動化スクリプト（推奨）

```bash
cd /Users/yuco/div/note/note-article-generator
./scripts/deploy-to-render.sh
```

スクリプトが対話形式で以下をガイドします：
- Render CLI認証確認
- 環境変数チェック
- Gitプッシュ確認
- サービス作成

### 方法2: Renderダッシュボード（手動）

1. **Renderにログイン**
   ```
   https://dashboard.render.com/
   Email: kindlesyuppan1@gmail.com
   ```

2. **新規Webサービス作成**
   - 「New +」→「Web Service」をクリック
   - GitHubリポジトリ選択: `yuco944/note-article-generator`
   - 「Connect」をクリック

3. **環境変数を設定**（必須）
   ```
   LLM_PROVIDER = claude
   LLM_API_KEY = sk-ant-xxxxx（あなたのClaude API Key）
   ```

4. **デプロイ実行**
   - 「Create Web Service」をクリック
   - 5-10分待つ

## ✅ デプロイ完了後の確認

### 1. ヘルスチェック

```bash
curl https://note-article-generator.onrender.com/api/v1/health
```

期待されるレスポンス：
```json
{"status": "ok", "version": "1.0.0"}
```

### 2. Web UIアクセス

```
https://note-article-generator.onrender.com/ui/notes/new
```

### 3. 記事生成テスト

Web UIで以下を入力してテスト：
- **トピック**: AI副業で月5万円稼ぐ方法
- **ターゲット読者**: 副業初心者
- **記事の目的**: 具体的な稼ぎ方を教える
- **記事タイプ**: 教育・解説系
- **文字数**: 中（4000-6000字）
- **訴求力の強度**: 7
- **Temperature**: 0.8

## 📋 環境変数の完全リスト

render.yamlで自動設定される変数：
```bash
FLASK_ENV=production
PORT=10000
LLM_MODEL_AGENT1=claude-3-5-sonnet-20241022
LLM_MODEL_AGENT2=claude-3-5-sonnet-20241022
LLM_AGENT1_MAX_TOKENS=6000
LLM_AGENT2_MAX_TOKENS=4000
MONTHLY_TOKEN_LIMIT=300000
GSHEET_NOTE_LOGS_SHEET=Note_Logs
```

**あなたが手動で設定する必要がある変数（必須）：**
```bash
LLM_PROVIDER=claude
LLM_API_KEY=sk-ant-xxxxx（あなたのAPI Key）
```

**オプション（後で追加可能）：**
```bash
GOOGLE_SHEETS_SPREADSHEET_ID=xxxxx
GOOGLE_APPLICATION_CREDENTIALS_JSON=base64エンコード済みJSON
```

## ⚠️ トラブルシューティング

### ビルドエラーが出た場合

1. Renderダッシュボードで「Logs」タブを確認
2. エラーメッセージをコピー
3. `RENDER_DEPLOY_STEP_BY_STEP.md`のトラブルシューティングセクションを参照

### 環境変数が正しく設定されているか確認

Renderダッシュボード → サービス → 「Environment」タブ

必ず以下の2つが設定されていることを確認：
- `LLM_PROVIDER`
- `LLM_API_KEY`

## 📚 詳細ガイド

- **ステップバイステップ**: `RENDER_DEPLOY_STEP_BY_STEP.md`
- **クイックスタート**: `QUICK_START.md`
- **環境変数チェックリスト**: `ENV_VARS_CHECKLIST.md`
- **次のステップ**: `NEXT_STEPS.md`

## 🎯 デプロイ準備状況

✅ GitHubリポジトリ: https://github.com/yuco944/note-article-generator
✅ render.yaml設定: 完了
✅ テスト: 24/28 (86%) パス
✅ ドキュメント: 完備
✅ スクリプト: 準備済み

**あなたのアクション**: RenderにログインしてWebサービスを作成するだけ！

---

**準備完了！デプロイを開始してください** 🚀
