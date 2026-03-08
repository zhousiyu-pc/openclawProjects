# 🛡️ Token 监控系统 - 安全备份指南

## ⚠️ 重要警告

### ❌ 这些位置会被阿里云系统重置清空：

```bash
/root/           # 系统重置会清空
/home/           # 系统重置会清空！
/opt/google/     # 可能也会被清理
```

### ✅ 哪些位置相对安全：

```bash
/opt/openclaw/   # OpenClaw 自己的配置目录（通常保留）
/data/           # 如果有独立数据盘则保留
/mnt/            # 挂载的外部磁盘（保留）
```

---

## 💾 推荐备份方案

### **方案一：上传到云端存储（最安全）**

```bash
# 1. 压缩备份
cd /home/admin/.openclaw/workspace
tar -czvf token-monitor-full-backup.tar.gz token-monitor/

# 2. 上传到对象存储（阿里云 OSS / AWS S3 / Cloudflare R2）
# 使用 ossutil 或 aws s3 cli
ossutil cp token-monitor-full-backup.tar.gz oss://your-bucket/backups/

# 或者用 rclone 同步到多个云盘
rclone copy token-monitor-full-backup.tar.gz remote:backups/
```

### **方案二：Git 版本控制（推荐）**

```bash
# 创建 Git 仓库
cd /home/admin/.openclaw/workspace
git init token-monitor-backup
git add token-monitor/
git commit -m "Token 监控系统完整备份"

# 推送到 GitHub/Gitee (私有仓库)
git remote add origin git@github.com:your-username/token-monitor-backup.git
git push -u origin main

# 恢复时只需克隆
git clone git@github.com:your-username/token-monitor-backup.git
```

### **方案三：双备份 + 本地快照**

```bash
# 本地备份 1：工作区
cp -r /home/admin/.openclaw/workspace/token-monitor \
       /home/admin/.openclaw/workspace/token-monitor.local.backup

# 本地备份 2：/tmp（重启后可能丢失，但有临时缓存）
cp /home/admin/.openclaw/workspace/token-monitor-full-backup.tar.gz \
       /tmp/token-monitor-backup.tar.gz

# 远程备份 3：OSS / S3 / Gist
./deploy.sh upload-to-cloud  # 需自行实现
```

### **方案四：使用阿里云快照（ECS 特色功能）**

```bash
# 这是阿里云 ECS 的官方快照功能
# 进入阿里云控制台 > 实例 > 快照
# 手动创建一个快照（免费，按容量收费）
# 即使服务器重装系统，也能从快照恢复！

# 或者用 CLI:
aliyun ecs CreateSnapshot --InstanceId i-xxx --Description "token-monitor-before-update"
```

---

## 📋 当前你的备份状态

检查现有备份：

```bash
# 查看当前备份文件
ls -lh /home/admin/.openclaw/workspace/token-monitor-full-backup.tar.gz

# 验证压缩包完整性
tar -tzf /home/admin/.openclaw/workspace/token-monitor-full-backup.tar.gz | head -10

# 显示大小
du -sh /home/admin/.openclaw/workspace/token-monitor/
```

预计输出：
```
-rw-r--r-- 1 admin admin 5.2K Mar 4 09:35 ...
drwxr-xr-x 3 admin admin 4.0K Mar 4 09:34 ...
Total: ~10KB（非常小！）
```

---

##  立即行动清单

### ✅ 已完成的备份：

- [x] `token-monitor-full-backup.tar.gz` - 完整备份包
- [x] `backup.sh` - 自动化备份脚本  
- [x] `BACKUP_GUIDE.md` - 恢复指南文档

### 🔒 建议补充的备份：

- [ ] **GitHub/Gitee**: 将备份推到私有仓库
- [ ] **阿里云 OSS**: 上传到对象存储
- [ ] **快照**: 在 ECS 控制台创建快照
- [ ] **邮件发送**: 定时把备份发到邮箱（可选）

---

## 🔧 一键备份命令

保存这个命令到你的 `.bashrc`:

```bash
# 添加到 ~/.bashrc
alias backup-token='cd ~/workspace && tar -czvf token-monitor-backup-$(date +%Y%m%d).tar.gz token-monitor/'

# 使生效
source ~/.bashrc

# 现在随便哪都能用了
backup-token
```

---

## 🆘 紧急情况下的恢复

如果服务器已经重装了，怎么办？

```bash
# 方法 1: 从云端下载
wget https://github.com/your-user/token-monitor-backup/archive/main.zip
unzip main.zip

# 方法 2: 从 OSS 下载
ossutil cp oss://your-bucket/token-monitor-backup.tar.gz .
tar -xzf token-monitor-backup.tar.gz

# 方法 3: 从旧服务器的快照恢复
# 在阿里云控制台：快照 -> 创建新实例
```

---

## 📊 总结

| 备份方式 | 安全性 | 成本 | 推荐度 |
|---------|--------|------|--------|
| 工作区本地 | ⭐⭐ | 免费 | ✅ |
| Git 仓库 | ⭐⭐⭐⭐⭐ | 免费 | ✅✅✅ |
| OSS/S3 | ⭐⭐⭐⭐ | ¥0.12/GB/月 | ✅✅ |
| ECS 快照 | ⭐⭐⭐⭐⭐ | ¥0.2/GB/月 | ✅✅✅ |
| 多重备份 | ⭐⭐⭐⭐⭐ | 低 | ✅✅✅✅✅ |

---

**Created by Your Assistant**  
**Last Updated**: 2026-03-04
