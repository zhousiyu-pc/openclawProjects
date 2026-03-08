#!/bin/bash
# Token 监控系统 - 快速部署/迁移脚本
# 用于在新服务器上快速恢复这套系统

set -e

echo "🚀 Token 监控系统部署脚本"
echo "========================="
echo ""

# 配置变量
WORKSPACE_DIR="/home/admin/.openclaw/workspace"
MONITOR_DIR="$WORKSPACE_DIR/token-monitor"
CONFIG_FILE="$MONITOR_DIR/config.json"
MODEL_STATE_FILE="$MONITOR_DIR/current-model.json"
LOG_FILE="/tmp/monitor.log"

# 检查 Node.js
echo "✅ 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js v14+"
    exit 1
fi
node_version=$(node --version)
echo "   Node.js: $node_version"
echo ""

# 创建目录
echo "📁 创建工作目录..."
mkdir -p "$MONITOR_DIR"
cd "$MONITOR_DIR"
echo "   工作目录：$MONITOR_DIR"
echo ""

# 读取当前配置文件（从备份或已存在的文件）
if [ -f "$CONFIG_FILE" ]; then
    echo "📋 使用现有配置文件："
    cat "$CONFIG_FILE" | head -20
    echo "   ..."
    echo ""
else
    echo "⚠️  未找到配置文件，请确保已复制完整的 token-monitor 文件夹"
    echo ""
    echo "需要包含的文件："
    echo "  - monitor.js (主程序)"
    echo "  - config.json (配置)"
    echo "  - README.md (文档)"
    exit 1
fi

# 确认 QQBot 用户 ID
echo "🔍 检查 QQBot 配置..."
QQ_USER_ID=$(grep -o '"qqUserId": "[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
if [ -z "$QQ_USER_ID" ]; then
    echo "⚠️  未找到 qqUserId 配置，请编辑 config.json 设置你的 QQ 用户 ID"
else
    echo "   QQ 用户 ID: $QQ_USER_ID"
fi
echo ""

# 停止旧进程
echo "⏹️  停止旧实例（如果有）..."
pkill -f "node monitor.js" 2>/dev/null || true
sleep 1
echo ""

# 启动服务
echo "▶️  启动 Token 监控服务..."
nohup node monitor.js > "$LOG_FILE" 2>&1 &
PID=$!
echo "   进程 PID: $PID"
echo "   日志文件：$LOG_FILE"
echo ""

# 等待启动
sleep 3
echo "📊 查看启动状态..."
tail -20 "$LOG_FILE"
echo ""

# 检查是否运行成功
if ps -p $PID > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "📋 下一步操作建议："
    echo "  1. 检查日志：tail -f $LOG_FILE"
    echo "  2. 查看用量：cat $MONITOR_DIR/usage-log.json"
    echo "  3. 查看当前模型：cat $MONITOR_DIR/current-model.json"
    echo "  4. 停止服务：pkill -f \"node monitor.js\""
    echo ""
    echo "💡 提示：如需开机自启，可配置 systemd 服务"
else
    echo "❌ 服务启动失败，请检查日志："
    cat "$LOG_FILE"
    exit 1
fi
