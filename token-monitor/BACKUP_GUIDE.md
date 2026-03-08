# Token 监控系统 - 备份与迁移指南

## 📦 完整备份清单

### 1. 核心配置文件

```bash
/home/admin/.openclaw/workspace/token-monitor/
├── monitor.js           # 主监控程序 (8203 bytes)
├── config.json          # 模型优先级配置 (1416 bytes)  
├── current-model.json   # 当前使用的模型状态 (191 bytes)
├── usage-log.json       # 用量统计日志 (动态生成)
├── README.md            # 使用说明 (2577 bytes)
├── STATUS.md            # 状态文档 (751 bytes)
└── BACKUP_GUIDE.md      # 本文件
```

### 2. 数据目录

```bash
# 用量记录文件（会被定期更新）
/home/admin/.openclaw/workspace/token-monitor/usage-log.json
/home/admin/.openclaw/workspace/token-monitor/current-model.json
```

---

## 🔄 系统恢复步骤

### 方式一：直接复制文件（最简单）

```bash
# 在新服务器上执行
cd /home/admin/.openclaw/workspace/

# 创建目录
mkdir -p token-monitor

# 复制所有文件到该目录
cp /path/to/backup/*.json token-monitor/
cp /path/to/backup/*.js token-monitor/
cp /path/to/backup/*.md token-monitor/

# 启动服务
cd token-monitor && nohup node monitor.js > /tmp/monitor.log 2>&1 &

# 验证运行状态
tail -f /tmp/monitor.log
```

### 方式二：使用 tar 打包还原

```bash
# 备份时创建压缩包
tar -czvf token-monitor-backup-$(date +%Y%m%d).tar.gz \
  token-monitor/

# 恢复时解压
tar -xzf token-monitor-backup-YYYYMMDD.tar.gz
cd token-monitor && nohup node monitor.js &
```

---

## 🔧 迁移到新服务器

### 1. 安装依赖

```bash
# 确认 Node.js 已安装
node --version  # 需要 v14+

# 检查工作区权限
ls -la ~/.openclaw/workspace/token-monitor/
```

### 2. 修改 QQBot 配置

如果新服务器的 QQBot 用户 ID 不同，需要修改：

```bash
# 编辑配置文件
vi token-monitor/config.json

# 修改这一行
"qqUserId": "新的 QQ 用户 ID"
```

或者设置环境变量：

```bash
export QQ_USER_ID="新的 QQ 用户 ID"
```

### 3. 调整路径（如果需要）

如果工作目录不同，检查以下文件中的路径：

```bash
# 检查 monitor.js 中的文件路径
grep -n "CURRENT_MODEL_FILE\|USAGE_LOG_FILE\|MODELS_CONFIG_FILE" \
  token-monitor/monitor.js
```

如有需要，编辑并替换为正确的路径。

---

## ⚙️ 配置说明

### modelPriority 配置

根据实际阿里云控制台情况调整：

```json
{
  "modelPriority": [
    {
      "provider": "dashscope",
      "modelId": "qwen3.5-flash-2026-02-23",  // 根据你的截图填写
      "hasFreeQuota": true,                    // true = 有免费额度
      "freeTokens": 1000000,                   // 可选：注明额度数量
      "description": "🏆 首选：百炼控制台 1M 额度"
    },
    // ... 其他备选模型
  ]
}
```

### 切换阈值设置

```json
{
  "settings": {
    "checkIntervalMinutes": 10,     // 检查频率
    "usageThresholdThousands": 50,  // 使用量阈值（k tokens）
    "budgetLimitYuan": 100          // 预算上限（元）
  }
}
```

---

## 📊 监控数据查看

### 实时日志

```bash
tail -f /tmp/monitor.log
```

### 历史用量

```bash
cat /home/admin/.openclaw/workspace/token-monitor/usage-log.json
```

示例输出：
```json
{
  "today": {
    "dashscope": 9412,
    "dashscope-us": 1912
  },
  "totalCost": 0.0012,
  "lastCheck": "2026-03-04T01:33:18Z"
}
```

### 当前模型状态

```bash
cat /home/admin/.openclaw/workspace/token-monitor/current-model.json
```

示例输出：
```json
{
  "provider": "dashscope",
  "modelId": "qwen3.5-flash-2026-02-23",
  "switchedAt": "2026-03-04T01:33:18Z",
  "reason": "✅ 新发现：百炼控制台有 1M 独立免费额度！"
}
```

---

## 🛠️ 常见问题

### Q1: 服务没有自动启动

**原因**: systemd 服务可能未配置

**解决**: 
```bash
# 手动启动
cd /home/admin/.openclaw/workspace/token-monitor
nohup node monitor.js > /tmp/monitor.log 2>&1 &

# 检查进程
ps aux | grep "node monitor"
```

### Q2: QQ 通知没收到

**原因**: 
- QQBot 用户 ID 不匹配
- 网络问题导致无法发送消息

**解决**:
```bash
# 检查配置
grep qqUserId config.json

# 临时调试：注释掉 sendQQNotification 函数
# 或手动测试 QQBot 连接
```

### Q3: 模型切换失败

**原因**: `models.json` 路径不对或权限不足

**解决**:
```bash
# 检查文件存在
ls -la /home/admin/.openclaw/agents/main/agent/models.json

# 尝试修复权限
chmod 644 /home/admin/.openclaw/agents/main/agent/models.json
```

---

## 📋 升级建议

当阿里云发布新版本或有新功能时：

1. **更新 modelPriority** - 添加新发现的额度充沛模型
2. **调整价格** - 根据最新定价更新 cost 字段
3. **优化阈值** - 根据实际情况调整使用量阈值

---

##  紧急处理

### 立即停止监控

```bash
pkill -f "node monitor.js"
```

### 重置为默认值

```bash
rm -f /home/admin/.openclaw/workspace/token-monitor/current-model.json
rm -f /home/admin/.openclaw/workspace/token-monitor/usage-log.json
```

### 完全卸载

```bash
pkill -f "node monitor.js" 2>/dev/null
rm -rf /home/admin/.openclaw/workspace/token-monitor/
```

---

## 📝 变更记录

- **2026-03-04 09:30** - 初始版本创建，集成百炼控制台额度发现
- **2026-03-04 09:32** - 切换到 qwen3.5-flash-2026-02-23 模型

---

**Created by Your Assistant**  
**Last Updated**: 2026-03-04 09:34 GMT+8
