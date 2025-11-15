# Renderデプロイ完全ガイド

## 📋 前提条件

以下を準備してください：

- [ ] GitHubアカウント
- [ ] Claude API Key（`sk-ant-`で始まる）
- [ ] Renderアカウント（無料）

## 🚀 ステップバイステップ手順

### ステップ1: Renderアカウント作成・ログイン

1. https://dashboard.render.com/ にアクセス
2. 「Get Started for Free」をクリック
3. **GitHub アカウント**でサインアップ/ログイン

### ステップ2: GitHubリポジトリを接続

1. Renderダッシュボードで **「New +」** ボタンをクリック
2. **「Web Service」** を選択
3. GitHubリポジトリ一覧から **「note-article-generator」** を探す
   - 見つからない場合: 「Configure account」でリポジトリアクセスを許可
4. **「Connect」** ボタンをクリック

### ステップ3: サービス設定

以下の設定を確認（render.yamlで自動設定されます）：

| 項目 | 値 |
|------|-----|
| **Name** | `note-article-generator` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app.main:app --bind 0.0.0.0:$PORT` |
| **Instance Type** | `Free` |

そのまま進んでOKです！

### ステップ4: 環境変数の設定（最重要！）

「Environment」セクションまでスクロールし、以下の環境変数を**手動で追加**：

#### 必須の環境変数

| Key | Value | 説明 |
|-----|-------|------|
| `LLM_PROVIDER` | `claude` | LLMプロバイダー |
| `LLM_API_KEY` | `sk-ant-xxxxxxxxx` | あなたのClaude API Key |

#### 環境変数の追加方法

1. 「Add Environment Variable」ボタンをクリック
2. **Key**: `LLM_PROVIDER`
3. **Value**: `claude`
4. 「Add」をクリック
5. 同様に `LLM_API_KEY` を追加（valueにAPI Keyを貼り付け）

### ステップ5: デプロイ実行

1. すべての設定を確認
2. **「Create Web Service」** ボタンをクリック
3. デプロイが開始されます（初回は5-10分かかります）

### ステップ6: デプロイ進行状況の確認

デプロイログが表示されます。以下のメッセージが表示されれば成功：

```
==> Build successful 🎉
==> Deploying...
==> Your service is live 🎉
```

### ステップ7: デプロイ完了後の動作確認

デプロイが完了すると、URLが表示されます：

```
https://note-article-generator.onrender.com
```

#### 7-1. ヘルスチェック

ターミナルで以下を実行：

```bash
curl https://note-article-generator.onrender.com/api/v1/health
```

期待されるレスポンス：

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### 7-2. Web UIにアクセス

ブラウザで以下にアクセス：

```
https://note-article-generator.onrender.com/ui/notes/new
```

記事生成フォームが表示されればOK！

#### 7-3. 記事生成テスト

1. Web UIで以下を入力：
   - **トピック**: `AI副業で月5万円稼ぐ方法`
   - **ターゲット読者**: `副業初心者`
   - **記事の目的**: `具体的な稼ぎ方を教える`
   - **記事タイプ**: `教育・解説系`
   - **文字数**: `中（4000-6000字）`
   - **訴求力の強度**: `7`
   - **Temperature**: `0.8`

2. 「生成開始」ボタンをクリック
3. 30秒〜1分で記事が生成されます

## 🔧 トラブルシューティング

### ❌ ビルドエラー: "requirements.txt not found"

**原因**: GitHubリポジトリが正しく接続されていない

**解決方法**:
1. Renderダッシュボードで該当サービスを削除
2. 再度「New Web Service」から作成
3. GitHubリポジトリの接続を確認

### ❌ 起動エラー: "Application failed to start"

**原因**: 環境変数が設定されていない

**解決方法**:
1. Renderダッシュボード → 該当サービス
2. 「Environment」タブをクリック
3. `LLM_PROVIDER`と`LLM_API_KEY`が設定されているか確認
4. 設定後、「Manual Deploy」→「Deploy latest commit」で再デプロイ

### ❌ API呼び出しエラー: "Claude API Error"

**原因**: API Keyが正しくない、またはクレジットが不足

**解決方法**:
1. https://console.anthropic.com/ でAPI Keyを確認
2. クレジット残高を確認
3. 必要に応じて新しいAPI Keyを発行
4. Renderの環境変数を更新
5. 再デプロイ

### ⚠️ アプリが起動しない（15分後にスリープ）

**これは正常です！**

- Render無料プランは15分間アクセスがないとスリープします
- 次回アクセス時に自動的に起動します（30秒程度かかります）

### 📝 ログの確認方法

1. Renderダッシュボード → 該当サービス
2. 「Logs」タブをクリック
3. リアルタイムログが表示されます

## 🎯 次のステップ

### オプション: Google Sheets連携（後で追加可能）

Google Sheets連携を追加する場合は `docs/deploy.md` の
「Google認証情報の設定」セクションを参照してください。

必要な環境変数：

```bash
GOOGLE_SHEETS_SPREADSHEET_ID=xxxxx
GOOGLE_APPLICATION_CREDENTIALS_JSON=base64エンコードされたJSON
```

### オプション: カスタムドメイン設定

1. Renderダッシュボード → 該当サービス
2. 「Settings」タブ
3. 「Custom Domain」セクションで独自ドメインを追加

## 📊 重要な情報

### 無料プランの制限

- **稼働時間**: 月750時間（約31日）
- **メモリ**: 512MB
- **CPU**: 共有
- **スリープ**: 15分間アクセスなしでスリープ
- **帯域幅**: 100GB/月

### コスト概算（有料プランへのアップグレード）

トラフィックが増えた場合：

- **Starter**: $7/月（常時起動、512MB）
- **Standard**: $25/月（常時起動、2GB）

## ✅ デプロイ完了チェックリスト

- [ ] Renderアカウント作成・ログイン完了
- [ ] GitHubリポジトリ接続完了
- [ ] 環境変数設定完了（`LLM_PROVIDER`, `LLM_API_KEY`）
- [ ] デプロイ成功（ログで確認）
- [ ] ヘルスチェックAPI動作確認
- [ ] Web UI表示確認
- [ ] 記事生成テスト成功

## 🆘 サポート

問題が解決しない場合：

1. **Renderのドキュメント**: https://render.com/docs
2. **このリポジトリのIssue**: https://github.com/yuco944/note-article-generator/issues

---

**デプロイ準備完了！** 上記の手順に従ってデプロイを進めてください 🚀
