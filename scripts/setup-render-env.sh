#!/bin/bash
#
# Render環境変数設定支援スクリプト
# このスクリプトはRenderに設定する環境変数を準備します
#

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Render 環境変数設定支援${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 環境変数の収集
echo -e "${YELLOW}Renderに設定する環境変数を入力してください${NC}"
echo "（Enterキーでスキップできます）"
echo ""

# LLM_API_KEY
read -p "LLM_API_KEY (Claude API Key): " LLM_API_KEY
if [ -n "$LLM_API_KEY" ]; then
    echo -e "${GREEN}✓ LLM_API_KEY を設定しました${NC}"
fi

# GOOGLE_SHEETS_SPREADSHEET_ID
read -p "GOOGLE_SHEETS_SPREADSHEET_ID: " GOOGLE_SHEETS_SPREADSHEET_ID
if [ -n "$GOOGLE_SHEETS_SPREADSHEET_ID" ]; then
    echo -e "${GREEN}✓ GOOGLE_SHEETS_SPREADSHEET_ID を設定しました${NC}"
fi

# GOOGLE_APPLICATION_CREDENTIALS_JSON
echo ""
echo -e "${YELLOW}Google認証情報ファイル（credentials.json）のパスを入力してください${NC}"
read -p "credentials.json のパス: " CREDENTIALS_PATH

if [ -n "$CREDENTIALS_PATH" ] && [ -f "$CREDENTIALS_PATH" ]; then
    # Base64エンコード
    GOOGLE_APPLICATION_CREDENTIALS_JSON=$(base64 < "$CREDENTIALS_PATH")
    echo -e "${GREEN}✓ credentials.json をBase64エンコードしました${NC}"
elif [ -n "$CREDENTIALS_PATH" ]; then
    echo -e "${RED}ファイルが見つかりません: $CREDENTIALS_PATH${NC}"
fi

# ADMIN_API_KEY
echo ""
read -p "ADMIN_API_KEY (ランダムな文字列、デフォルト: 自動生成): " ADMIN_API_KEY
if [ -z "$ADMIN_API_KEY" ]; then
    ADMIN_API_KEY=$(openssl rand -hex 32)
    echo -e "${GREEN}✓ ADMIN_API_KEY を自動生成しました${NC}"
fi

# 環境変数ファイルの生成
echo ""
echo -e "${YELLOW}環境変数設定ファイルを生成します...${NC}"

ENV_FILE="$PROJECT_ROOT/render-env-vars.txt"
cat > "$ENV_FILE" << EOF
# Render環境変数設定
# 以下の環境変数をRenderダッシュボードで設定してください
# https://dashboard.render.com/

# Flask設定
FLASK_ENV=production
PORT=10000

# LLM設定
LLM_PROVIDER=claude
LLM_API_KEY=${LLM_API_KEY:-<YOUR_CLAUDE_API_KEY>}
LLM_MODEL_AGENT1=claude-3-5-sonnet-20241022
LLM_MODEL_AGENT2=claude-3-5-sonnet-20241022
LLM_AGENT1_MAX_TOKENS=6000
LLM_AGENT2_MAX_TOKENS=4000

# Google Sheets設定
GOOGLE_SHEETS_SPREADSHEET_ID=${GOOGLE_SHEETS_SPREADSHEET_ID:-<YOUR_SPREADSHEET_ID>}
GSHEET_NOTE_LOGS_SHEET=Note_Logs
GOOGLE_APPLICATION_CREDENTIALS_JSON=${GOOGLE_APPLICATION_CREDENTIALS_JSON:-<BASE64_ENCODED_CREDENTIALS>}

# アプリケーション設定
ADMIN_API_KEY=${ADMIN_API_KEY}
MONTHLY_TOKEN_LIMIT=300000
EOF

echo -e "${GREEN}✓ 環境変数ファイルを生成しました: $ENV_FILE${NC}"
echo ""

# Render CLIを使用して環境変数を設定する場合
if command -v render &> /dev/null; then
    echo -e "${YELLOW}Render CLIを使用して環境変数を設定しますか？${NC}"
    read -p "(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "サービスIDを入力してください: " SERVICE_ID
        if [ -n "$SERVICE_ID" ]; then
            echo "環境変数を設定しています..."
            
            if [ -n "${LLM_API_KEY:-}" ]; then
                render env set LLM_API_KEY="$LLM_API_KEY" --service "$SERVICE_ID"
            fi
            
            if [ -n "${GOOGLE_SHEETS_SPREADSHEET_ID:-}" ]; then
                render env set GOOGLE_SHEETS_SPREADSHEET_ID="$GOOGLE_SHEETS_SPREADSHEET_ID" --service "$SERVICE_ID"
            fi
            
            if [ -n "${GOOGLE_APPLICATION_CREDENTIALS_JSON:-}" ]; then
                render env set GOOGLE_APPLICATION_CREDENTIALS_JSON="$GOOGLE_APPLICATION_CREDENTIALS_JSON" --service "$SERVICE_ID"
            fi
            
            render env set ADMIN_API_KEY="$ADMIN_API_KEY" --service "$SERVICE_ID"
            
            echo -e "${GREEN}✓ 環境変数を設定しました${NC}"
        fi
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}環境変数設定が完了しました！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "次のステップ:"
echo "  1. 生成されたファイルを確認: $ENV_FILE"
echo "  2. Renderダッシュボードで環境変数を設定:"
echo "     https://dashboard.render.com/"
echo "  3. または、Render CLIを使用:"
echo "     render env set KEY=value --service <SERVICE_ID>"
echo ""

