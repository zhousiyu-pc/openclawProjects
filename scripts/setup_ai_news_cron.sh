#!/bin/bash
# 设置每天 9 点的 AI 新闻定时任务
CRON_EXPR="0 9 * * *"

# 创建一个 AI agent 任务来执行新闻搜索和发送
TASK_CMD="openclaw sessions_spawn --task '搜索今天评论最多的 10 条 AI 新闻，汇总后发送到 120839976@qq.com' --mode run 2>&1 >> /tmp/ai_news.log"

# 添加到 crontab
(crontab -l 2>/dev/null | grep -v "daily_ai_news"; echo "$CRON_EXPR $TASK_CMD") | crontab -

echo "✅ AI 新闻定时任务已设置（每天 9 点）"
crontab -l | grep -E "ai|news"
