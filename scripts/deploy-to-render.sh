#!/bin/bash
#
# Renderへのデプロイスクリプト
# このスクリプトはRenderへのデプロイを自動化します
#

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Render デプロイスクリプト${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Render CLIのインストール確認
echo -e "${YELLOW}[1/6] Render CLIの確認...${NC}"
if ! command -v render &> /dev/null; then
    echo -e "${YELLOW}Render CLIが見つかりません。インストールします...${NC}"
    
    # macOSの場合
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Homebrewを使用してインストールします..."
            brew install render
        else
            echo -e "${RED}Homebrewがインストールされていません。${NC}"
            echo "以下のコマンドで手動インストールしてください:"
            echo "  brew install render"
            exit 1
        fi
    else
        echo -e "${RED}このOSでは自動インストールをサポートしていません。${NC}"
        echo "以下のURLから手動でインストールしてください:"
        echo "  https://render.com/docs/cli"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Render CLIは既にインストールされています${NC}"
fi

# 2. 認証確認
echo ""
echo -e "${YELLOW}[2/6] Render認証の確認...${NC}"
if ! render whoami &> /dev/null; then
    echo -e "${YELLOW}Renderにログインしていません。${NC}"
    echo "以下のコマンドでログインしてください:"
    echo "  render login"
    echo ""
    read -p "今すぐログインしますか？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        render login
    else
        echo -e "${RED}認証が必要です。後で実行してください。${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Renderに認証済み${NC}"
    render whoami
fi

# 3. 必須環境変数の確認
echo ""
echo -e "${YELLOW}[3/6] 環境変数の確認...${NC}"
REQUIRED_VARS=(
    "LLM_API_KEY"
    "GOOGLE_SHEETS_SPREADSHEET_ID"
)

MISSING_VARS=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var:-}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${RED}以下の環境変数が設定されていません:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "環境変数を設定するか、.envファイルに追加してください。"
    echo "または、Renderダッシュボードで環境変数を設定してください。"
    echo ""
    read -p "続行しますか？（環境変数は後で設定できます）(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ 必須環境変数が設定されています${NC}"
fi

# 4. render.yamlの確認
echo ""
echo -e "${YELLOW}[4/6] render.yamlの確認...${NC}"
if [ ! -f "render.yaml" ]; then
    echo -e "${RED}render.yamlが見つかりません${NC}"
    exit 1
fi
echo -e "${GREEN}✓ render.yamlが見つかりました${NC}"

# 5. Gitリポジトリの確認
echo ""
echo -e "${YELLOW}[5/6] Gitリポジトリの確認...${NC}"
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Gitリポジトリが初期化されていません。${NC}"
    read -p "Gitリポジトリを初期化しますか？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit for Render deployment"
        echo -e "${GREEN}✓ Gitリポジトリを初期化しました${NC}"
        echo ""
        echo -e "${YELLOW}GitHubにリポジトリを作成し、以下のコマンドでプッシュしてください:${NC}"
        echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "  git push -u origin main"
        echo ""
        read -p "GitHubリポジトリを既に作成済みで、今すぐプッシュしますか？ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "GitHubリポジトリURLを入力してください: " REPO_URL
            git remote add origin "$REPO_URL"
            git branch -M main
            git push -u origin main
        fi
    else
        echo -e "${RED}Gitリポジトリが必要です。${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Gitリポジトリが見つかりました${NC}"
    
    # 変更があるか確認
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}未コミットの変更があります。${NC}"
        git status --short
        echo ""
        read -p "変更をコミットしてプッシュしますか？ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "コミットメッセージを入力してください（デフォルト: Deploy to Render）: " COMMIT_MSG
            COMMIT_MSG=${COMMIT_MSG:-"Deploy to Render"}
            git commit -m "$COMMIT_MSG"
            
            # リモートがあるか確認
            if git remote | grep -q origin; then
                echo "リモートリポジトリにプッシュします..."
                git push
            else
                echo -e "${YELLOW}リモートリポジトリが設定されていません。${NC}"
                read -p "GitHubリポジトリURLを入力してください: " REPO_URL
                git remote add origin "$REPO_URL"
                git push -u origin main
            fi
        fi
    else
        echo -e "${GREEN}✓ 変更はありません${NC}"
    fi
fi

# 6. Renderサービス作成/更新
echo ""
echo -e "${YELLOW}[6/6] Renderサービスの作成/更新...${NC}"
echo ""
echo "以下のオプションから選択してください:"
echo "  1) 新しいWebサービスを作成（初回デプロイ）"
echo "  2) 既存のサービスを更新"
echo "  3) render.yamlを使用してサービスを適用"
read -p "選択 (1/2/3): " -n 1 -r
echo ""

case $REPLY in
    1)
        echo -e "${BLUE}新しいWebサービスを作成します...${NC}"
        echo ""
        echo "GitHubリポジトリを選択する必要があります。"
        echo "Renderダッシュボードで手動で作成するか、以下を実行してください:"
        echo ""
        echo "  render services create web --name note-article-generator \\"
        echo "    --repo https://github.com/YOUR_USERNAME/YOUR_REPO.git \\"
        echo "    --branch main \\"
        echo "    --region oregon \\"
        echo "    --plan free"
        echo ""
        echo "または、Renderダッシュボードで以下を実行:"
        echo "  1. https://dashboard.render.com/ にアクセス"
        echo "  2. 'New +' → 'Web Service' を選択"
        echo "  3. GitHubリポジトリを選択"
        echo "  4. 環境変数を設定（LLM_API_KEYなど）"
        echo "  5. 'Create Web Service' をクリック"
        ;;
    2)
        echo -e "${BLUE}既存のサービスを更新します...${NC}"
        render services list
        echo ""
        read -p "更新するサービスIDを入力してください: " SERVICE_ID
        render services update "$SERVICE_ID" --name note-article-generator
        ;;
    3)
        echo -e "${BLUE}render.yamlを使用してサービスを適用します...${NC}"
        render blueprint apply
        ;;
    *)
        echo -e "${RED}無効な選択です${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}デプロイ手順が完了しました！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "次のステップ:"
echo "  1. Renderダッシュボードで環境変数を設定:"
echo "     - LLM_API_KEY (Claude API Key)"
echo "     - GOOGLE_SHEETS_SPREADSHEET_ID"
echo "     - GOOGLE_APPLICATION_CREDENTIALS_JSON (Base64エンコード)"
echo ""
echo "  2. デプロイの進行状況を確認:"
echo "     https://dashboard.render.com/"
echo ""
echo "  3. デプロイ完了後、ヘルスチェック:"
echo "     curl https://note-article-generator.onrender.com/api/v1/health"
echo ""

