#!/bin/bash

echo "=== Note記事生成APIテスト ==="
echo ""

# サーバー起動（バックグラウンド）
export PYTHONPATH=/Users/yuco/div/note/note-article-generator:$PYTHONPATH
python3 app/main.py > /dev/null 2>&1 &
SERVER_PID=$!

echo "サーバー起動中...（PID: $SERVER_PID）"
sleep 10

echo ""
echo "==== TEST 1: Health Check ===="
curl -s http://localhost:8000/api/v1/health | python3 -m json.tool
echo ""

echo "==== TEST 2: Generate Note (正常系) ===="
curl -s -X POST http://localhost:8000/api/v1/notes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI副業で月5万円稼ぐ方法",
    "audience": "副業初心者",
    "goal": "具体的な稼ぎ方を教える",
    "article_type": "education",
    "length_class": "middle",
    "temperature": 0.8,
    "intensity_level": 7
  }' | python3 -m json.tool | head -50
echo ""

echo "==== TEST 3: Generate Note (異常系: temperature範囲外) ===="
curl -s -X POST http://localhost:8000/api/v1/notes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "test",
    "audience": "test",
    "goal": "test",
    "article_type": "education",
    "length_class": "middle",
    "temperature": 3.0,
    "intensity_level": 5
  }' | python3 -m json.tool
echo ""

echo "==== TEST 4: List Notes ===="
curl -s http://localhost:8000/api/v1/notes | python3 -m json.tool
echo ""

echo "サーバー停止中..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "テスト完了"
