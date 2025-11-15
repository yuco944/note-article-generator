# 502 Bad Gateway エラーの対処法

## 🔍 現在の状況

URL `https://note-article-generator.onrender.com` にアクセスすると、502 Bad Gatewayエラーが表示されています。

## 📋 考えられる原因と対処法

### 1. サービスがスリープしている（無料プラン）

**原因**: Renderの無料プランは、15分間アクセスがないと自動的にスリープします。

**対処法**:
1. 30秒〜1分待ってから再度アクセス
2. 初回アクセス時は起動に時間がかかります

**確認方法**:
- Renderダッシュボードでサービスの状態を確認
- 「Live」と表示されていれば起動中

---

### 2. 環境変数が設定されていない

**原因**: 必須の環境変数（特に`LLM_API_KEY`）が設定されていない

**対処法**:
1. Renderダッシュボードにアクセス
2. 該当サービスを選択
3. 「Environment」タブをクリック
4. 以下の環境変数が設定されているか確認：
   - `LLM_PROVIDER` = `claude`
   - `LLM_API_KEY` = （あなたのAPI Key）
5. 設定後、「Manual Deploy」→「Deploy latest commit」で再デプロイ

---

### 3. ビルドエラー

**原因**: 依存パッケージのインストールに失敗している

**確認方法**:
1. Renderダッシュボード → 該当サービス
2. 「Logs」タブをクリック
3. ビルドログを確認

**よくあるエラー**:
- `requirements.txt` が見つからない
- Pythonバージョンの不一致
- 依存パッケージのインストールエラー

**対処法**:
- エラーメッセージを確認
- `requirements.txt` の内容を確認
- 必要に応じて `runtime.txt` でPythonバージョンを指定

---

### 4. アプリケーション起動エラー

**原因**: アプリケーションが起動できない

**確認方法**:
1. Renderダッシュボード → 該当サービス
2. 「Logs」タブをクリック
3. 起動ログを確認

**よくあるエラー**:
- 環境変数が不足している
- ポート番号の設定ミス
- アプリケーションコードのエラー

**対処法**:
- エラーメッセージを確認
- 環境変数を再確認
- ローカルで動作確認

---

## 🔧 ステップバイステップ対処手順

### ステップ1: Renderダッシュボードで状態確認

1. [Render Dashboard](https://dashboard.render.com/) にアクセス
2. `note-article-generator` サービスを選択
3. サービスの状態を確認：
   - **「Live」** = 起動中（正常）
   - **「Sleeping」** = スリープ中（次回アクセスで自動起動）
   - **「Build failed」** = ビルドエラー
   - **「Deploy failed」** = デプロイエラー

### ステップ2: ログを確認

1. 「Logs」タブをクリック
2. 最新のログを確認
3. エラーメッセージを探す

### ステップ3: 環境変数を確認

1. 「Environment」タブをクリック
2. 必須の環境変数が設定されているか確認：
   ```
   LLM_PROVIDER=claude
   LLM_API_KEY=（あなたのAPI Key）
   ```

### ステップ4: 再デプロイ

1. 「Manual Deploy」をクリック
2. 「Deploy latest commit」を選択
3. デプロイが完了するまで待つ（5-10分）

---

## ✅ 正常な状態の確認方法

デプロイが成功すると、以下のように動作します：

### ヘルスチェック

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

### Web UI

ブラウザで以下にアクセス：
```
https://note-article-generator.onrender.com/ui/notes/new
```

記事生成フォームが表示されれば成功です！

---

## 🆘 それでも解決しない場合

1. **ログを共有**: Renderダッシュボードのログをコピー
2. **環境変数を確認**: すべての環境変数が正しく設定されているか
3. **ローカルでテスト**: 同じ環境変数でローカルで動作確認

---

## 📝 参考

- [Render公式ドキュメント - トラブルシューティング](https://render.com/docs/troubleshooting-deploys#502-bad-gateway)
- [デプロイガイド](RENDER_DEPLOY_STEP_BY_STEP.md)

