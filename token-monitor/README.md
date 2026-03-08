# Token 监控系统

## 📋 功能说明

这是一个独立的 Token 使用量监控服务，具有以下特性：

### 核心功能
- ✅ **自动监控**: 每 10 分钟检查一次 token 使用量
- ✅ **智能切换**: 优先切换到有免费额度的模型
- ✅ **成本估算**: 实时计算预估费用
- ✅ **QQBot 通知**: 关键事件自动发送 QQ 消息提醒

### ⚠️ 当前状态

**所有 DashScope 模型的免费额度可能已用完！**

当前优先级列表：
1. `qwen3.5-plus-2026-02-15` - 尝试这个旧版本，可能还有独立额度
2. `qwen3.5-flash-2026-02-23` - Flash 新版本，可能有独立额度
3. `qwen3.5-plus` - 已知用完 ❌
4. `qwen3.5-flash` - 已知用完 ❌
5. `qwen3-max-2025-09-23` - 海外版（需要确认是否收费）

## 🔧 快速启动

```bash
cd /home/admin/.openclaw/workspace/token-monitor
node monitor.js &
```

## 📊 监控数据

- 使用量阈值：50k tokens
- 预算上限：￥100
- 检查间隔：10 分钟

---

_created by Your Assistant_  
_Last updated: 2026-03-04_
