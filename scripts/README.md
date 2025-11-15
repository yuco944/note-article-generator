# デプロイスクリプト

このディレクトリには、Renderへのデプロイを支援するスクリプトが含まれています。

## スクリプト一覧

### `setup-render-env.sh`

Renderに設定する環境変数を準備するスクリプトです。

**機能:**
- 必要な環境変数の対話式入力
- Google認証情報ファイルのBase64エンコード
- 環境変数設定ファイルの生成
- Render CLIを使用した環境変数の自動設定（オプション）

**使用方法:**
```bash
./scripts/setup-render-env.sh
```

**出力:**
- `render-env-vars.txt`: Renderダッシュボードで設定する環境変数のリスト

### `deploy-to-render.sh`

Renderへのデプロイを自動化するスクリプトです。

**機能:**
- Render CLIのインストール確認・インストール
- Render認証の確認
- 必須環境変数の確認
- Gitリポジトリの確認・初期化
- 変更の自動コミット・プッシュ
- Renderサービスの作成/更新

**使用方法:**
```bash
./scripts/deploy-to-render.sh
```

**前提条件:**
- GitHubリポジトリが作成されていること（初回デプロイの場合）
- Renderアカウントが作成されていること
- 必要な環境変数が設定されていること（または後で設定可能）

## デプロイフロー

### 初回デプロイ

1. **GitHubリポジトリの作成**
   ```bash
   # GitHubでリポジトリを作成後
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **環境変数の準備**
   ```bash
   ./scripts/setup-render-env.sh
   ```

3. **RenderダッシュボードでWebサービスを作成**
   - https://dashboard.render.com/ にアクセス
   - "New +" → "Web Service" を選択
   - GitHubリポジトリを選択
   - 環境変数を設定（`render-env-vars.txt`を参照）

4. **デプロイスクリプトの実行（オプション）**
   ```bash
   ./scripts/deploy-to-render.sh
   ```

### 更新デプロイ

1. **変更をコミット・プッシュ**
   ```bash
   git add .
   git commit -m "Update"
   git push
   ```

2. **Renderが自動的にデプロイ**
   - GitHubにプッシュすると、Renderが自動的にデプロイを開始します

## トラブルシューティング

### Render CLIが見つからない

macOSの場合:
```bash
brew install render
```

その他のOS:
- https://render.com/docs/cli から手動でインストール

### 認証エラー

```bash
render auth login
```

### 環境変数が設定されていない

`setup-render-env.sh`を実行して環境変数を準備するか、Renderダッシュボードで手動で設定してください。

## 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [Render CLIドキュメント](https://render.com/docs/cli)
- [デプロイ手順詳細](../docs/deploy.md)

