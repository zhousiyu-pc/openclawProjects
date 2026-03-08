#!/bin/bash
# Token 监控系统 - 完整备份脚本

set -e

BACKUP_DIR="/home/admin/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="token-monitor-$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo "📦 Token 监控系统备份"
echo "====================="
echo ""

# 创建备份目录
mkdir -p "$BACKUP_PATH"
echo "📁 备份路径：$BACKUP_PATH"
echo ""

# 复制核心文件
SOURCE_DIR="/home/admin/.openclaw/workspace/token-monitor"
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ 未找到监控目录：$SOURCE_DIR"
    exit 1
fi

echo "📋 复制文件..."
cp -r "$SOURCE_DIR"/* "$BACKUP_PATH/"
echo "   ✅ 已复制所有文件"
echo ""

# 生成备份清单
cat > "$BACKUP_PATH/MANIFEST.txt" << EOF
Token 监控系统备份
==================
备份时间：$(date)
来源目录：$SOURCE_DIR
文件列表:
EOF

find "$BACKUP_PATH" -type f | sort >> "$BACKUP_PATH/MANIFEST.txt"

# 显示统计信息
FILE_COUNT=$(find "$BACKUP_PATH" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_PATH" | cut -f1)

echo "📊 备份统计:"
echo "   文件数量：$FILE_COUNT"
echo "   总大小：$TOTAL_SIZE"
echo ""

# 创建压缩包
echo "💾 创建压缩包..."
cd "$BACKUP_DIR"
tar -czvf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME/"
rm -rf "$BACKUP_NAME"
echo "   压缩包：$BACKUP_NAME.tar.gz"
echo ""

# 显示文件详情
echo "📄 MANIFEST 内容:"
cat "$BACKUP_PATH/../MANIFEST.txt" 2>/dev/null || echo "   (无 manifest)"
echo ""

echo "✅ 备份完成！"
echo ""
echo "📍 备份位置：$BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo ""
echo "💡 恢复方法："
echo "   tar -xzf $BACKUP_NAME.tar.gz -C /home/admin/.openclaw/workspace/"
echo "   cd token-monitor && nohup node monitor.js &"
