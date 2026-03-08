# 🦞 OpenClaw 系统升级与恢复指南

## 📋 升级前准备

### 1. 备份当前配置
```bash
# 运行一键备份脚本
/home/admin/.openclaw/workspace/scripts/backup_workspace.sh

# 手动备份关键配置
tar -czf /data/openclaw/full_backup_$(date +%Y%m%d).tar.gz \
  ~/.openclaw/models.json \
  ~/.openclaw/model_state.json \
  /home/admin/.openclaw/workspace/scripts/
```

### 2. 记录当前状态
```bash
# 查看当前配置
openclaw status
crontab -l
cat ~/.openclaw/models.json

# 截图或保存输出到文件
openclaw status > /data/openclaw/pre_upgrade_status.txt
```

---

## 🔄 系统升级场景

### 场景 A: OpenClaw 软件升级
```bash
# 升级 OpenClaw
npm update -g openclaw

# 或从源码更新
cd /opt/openclaw && git pull && npm install

# 验证升级
openclaw --version
openclaw status
```

**恢复步骤:**
```bash
# 通常不需要恢复，配置会自动保留
# 如有问题，运行恢复脚本
/home/admin/.openclaw/workspace/scripts/restore_config.sh
```

---

### 场景 B: 操作系统升级/重装（阿里云）

#### 升级前:
```bash
# 1. 确保 /data 目录在独立分区（不会被格式化）
df -h /data

# 2. 备份所有配置到 /data
/home/admin/.openclaw/workspace/scripts/restore_config.sh
# 这会自动备份配置到 /data/openclaw/

# 3. 导出 crontab
crontab -l > /data/openclaw/crontab_backup.txt

# 4. 创建升级检查清单
cat > /data/openclaw/UPGRADE_CHECKLIST.md << EOF
# 升级检查清单

## 升级后需要执行:
1. 运行恢复脚本：./restore_config.sh
2. 验证模型配置：cat ~/.openclaw/models.json
3. 验证 cron 任务：crontab -l
4. 测试备份功能：./backup_workspace.sh
5. 测试切换功能：./auto_switch_model.sh status
EOF
```

#### 升级后:
```bash
# 1. 恢复配置
/home/admin/.openclaw/workspace/scripts/restore_config.sh

# 2. 验证所有功能
openclaw status
crontab -l
/home/admin/.openclaw/workspace/scripts/token_monitor.sh

# 3. 检查日志
tail -20 /var/log/openclaw-token-monitor.log
```

---

### 场景 C: Docker 容器重建

#### 使用持久化卷:
```bash
# 启动容器时挂载数据卷
docker run -d \
  -v /data/openclaw:/data/openclaw \
  -v ~/.openclaw:/root/.openclaw \
  -v /var/log/openclaw:/var/log/openclaw \
  --name openclaw \
  openclaw:latest

# 进入容器恢复配置
docker exec -it openclaw bash
/home/admin/.openclaw/workspace/scripts/restore_config.sh
```

---

## 🛠️ 恢复脚本详解

### 一键恢复命令
```bash
/home/admin/.openclaw/workspace/scripts/restore_config.sh
```

### 恢复内容包括:
| 项目 | 恢复方式 |
|------|----------|
| ✅ 模型配置 | 从 `/data/openclaw/models.json` 恢复 |
| ✅ Cron 任务 | 自动检测并添加缺失任务 |
| ✅ 脚本权限 | `chmod +x` 所有脚本 |
| ✅ 日志文件 | 创建并设置权限 |
| ✅ 配置文件备份 | 同步到 `/data/openclaw/` |

---

## 📁 关键文件位置

### 持久化数据（系统升级后保留）
```
/data/openclaw/
├── workspace/          # Workspace 完整备份
├── backups/            # 自动备份文件
├── models.json         # 模型配置备份
└── model_state.json    # 模型状态备份
```

### 系统配置（可能丢失，需恢复）
```
~/.openclaw/
├── models.json         # 当前模型配置
└── model_state.json    # 当前模型状态

/var/log/
├── openclaw-backup.log
├── openclaw-token-monitor.log
└── openclaw-model-switch.log
```

---

## ✅ 升级后验证清单

```bash
# 1. OpenClaw 状态
openclaw status

# 2. 模型配置
cat ~/.openclaw/models.json

# 3. Cron 任务
crontab -l

# 4. Token 监控
/home/admin/.openclaw/workspace/scripts/token_monitor.sh

# 5. 模型切换
/home/admin/.openclaw/workspace/scripts/auto_switch_model.sh status

# 6. 日志文件
ls -lh /var/log/openclaw-*.log

# 7. 备份目录
ls -lh /data/openclaw/backups/
```

---

## 🚨 故障排查

### 问题：恢复脚本报错
```bash
# 检查脚本是否存在
ls -la /home/admin/.openclaw/workspace/scripts/restore_config.sh

# 手动执行恢复步骤
source /home/admin/.openclaw/workspace/scripts/restore_config.sh
restore_model_config
restore_cron_jobs
```

### 问题：Cron 任务丢失
```bash
# 手动添加
echo "0 3 * * * /home/admin/.openclaw/workspace/scripts/backup_workspace.sh" | crontab -
echo "0 */6 * * * /home/admin/.openclaw/workspace/scripts/token_monitor.sh" | crontab -
```

### 问题：模型配置丢失
```bash
# 从备份恢复
cp /data/openclaw/models.json ~/.openclaw/models.json

# 或创建默认配置
echo '{"default_model": "dashscope/qwen3.5-plus-2026-02-15"}' > ~/.openclaw/models.json
```

---

## 📞 需要帮助？

1. 查看日志：`tail -f /var/log/openclaw-token-monitor.log`
2. 检查文档：`/home/admin/.openclaw/workspace/scripts/MODEL_MANAGEMENT.md`
3. 运行诊断：`openclaw status`

---

**记住：所有重要数据都备份在 `/data/openclaw/`，系统重装也不怕！** 🎉
