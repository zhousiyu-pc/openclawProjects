#!/bin/bash
# 记忆备份脚本 - 备份 workspace 到指定目录或远程

WORKSPACE_DIR="/home/admin/.openclaw/workspace"
BACKUP_DIR="/home/admin/.openclaw/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份整个 workspace
BACKUP_FILE="$BACKUP_DIR/workspace_backup_$DATE.tar.gz"
tar -czf "$BACKUP_FILE" -C "$(dirname $WORKSPACE_DIR)" "$(basename $WORKSPACE_DIR)"

echo "✅ 备份完成：$BACKUP_FILE"

# 可选：同步到远程服务器 (取消注释并配置)
# rsync -avz "$BACKUP_FILE" user@remote:/path/to/backups/

# 清理 30 天前的旧备份
find "$BACKUP_DIR" -name "workspace_backup_*.tar.gz" -mtime +30 -delete

echo "🗑️ 已清理 30 天前的旧备份"
