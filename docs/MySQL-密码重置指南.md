# 📋 Mac 忘记 MySQL root 密码 - 完整重置指南

> 创建日期：2026-03-07  
> 适用系统：macOS + MySQL 8.0+（官方 DMG 安装包）

---

## ⚠️ 问题场景

- 忘记 MySQL root 密码
- Mac 系统（官方 DMG 安装包）
- MySQL 服务由 launchd 管理，进程会自动重启

---

## 🔍 第 1 步：确认 MySQL 安装方式

```bash
# 检查安装路径
ls /usr/local/mysql          # 官方安装包
ls /opt/homebrew/opt/mysql   # Homebrew 安装

# 检查运行中的进程
ps aux | grep mysql
```

**本例情况**：官方 DMG 安装在 `/usr/local/mysql`

---

## 🛑 第 2 步：停止 MySQL 服务

```bash
# 1. 查找 launchd 服务名
sudo launchctl list | grep -i mysql
# 输出示例：52058 -9 com.oracle.oss.mysql.mysqld

# 2. 停止服务（用正确的服务名）
sudo launchctl remove com.oracle.oss.mysql.mysqld

# 3. 杀掉所有 mysqld 进程
sudo pkill -9 mysqld

# 4. 确认已停止
ps aux | grep mysql
# 应该只有 grep mysql，没有 mysqld
```

---

## 🔓 第 3 步：跳过权限验证启动 MySQL

```bash
# 后台启动（跳过密码验证）
sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables --skip-networking &

# 等待启动
sleep 5

# 免密登录
mysql -u root
```

---

## 🔑 第 4 步：重置 root 密码

```sql
-- 进入 MySQL 命令行后执行

-- 1. 刷新权限
FLUSH PRIVILEGES;

-- 2. 修改密码（MySQL 8.0+）
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';

-- 3. 退出
EXIT;
```

**注意**：
- MySQL 8.0+ 不支持 `mysql_native_password` 插件
- MySQL 8.0+ 已移除 `PASSWORD()` 函数
- 直接用 `IDENTIFIED BY '密码'` 即可

---

## 🔄 第 5 步：重启 MySQL 服务

```bash
# 1. 杀掉跳过权限的进程
sudo pkill -9 mysqld

# 2. 恢复服务（三选一）

# 方法 A：用 mysql.server 脚本（推荐）
sudo /usr/local/mysql/support-files/mysql.server start

# 方法 B：用 launchctl bootstrap
sudo launchctl bootstrap system /Library/LaunchDaemons/com.oracle.oss.mysql.plist

# 方法 C：系统偏好设置里手动启动
```

---

## ✅ 第 6 步：验证新密码

```bash
mysql -u root -p
# 输入新密码
```

---

## 📌 关键命令速查

| 步骤 | 命令 |
|------|------|
| 查服务名 | `sudo launchctl list \| grep -i mysql` |
| 停止服务 | `sudo launchctl remove <服务名>` |
| 杀进程 | `sudo pkill -9 mysqld` |
| 跳过权限启动 | `sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables --skip-networking &` |
| 重置密码 | `ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';` |
| 启动服务 | `sudo /usr/local/mysql/support-files/mysql.server start` |

---

## ⚠️ 常见问题

| 问题 | 解决 |
|------|------|
| 进程自动重启 | 先用 `launchctl remove` 停止服务，再杀进程 |
| `mysql_native_password` 报错 | MySQL 8.0+ 直接用 `IDENTIFIED BY '密码'` |
| `PASSWORD()` 函数报错 | MySQL 8.0+ 已移除，不用这个函数 |
| `launchctl load` 失败 | 改用 `launchctl bootstrap` 或 `mysql.server start` |
| 找不到 mysqld_safe | 用完整路径 `/usr/local/mysql/bin/mysqld_safe` |

---

## 🛡️ 安全建议

```sql
-- 1. 创建日常使用的普通用户
CREATE USER 'admin'@'localhost' IDENTIFIED BY '强密码';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;

-- 2. 限制 root 只能本地登录
DROP USER 'root'@'%';

-- 3. 删除匿名用户
DELETE FROM mysql.user WHERE User='';

-- 4. 检查用户权限
SELECT user, host, plugin FROM mysql.user;
```

---

## 📝 本次重置记录

| 项目 | 值 |
|------|-----|
| 日期 | 2026-03-07 |
| 系统 | macOS (Apple Silicon) |
| MySQL 路径 | `/usr/local/mysql` |
| 服务名 | `com.oracle.oss.mysql.mysqld` |
| 新密码 | `Sinolife2008` |

---

## 💾 备份建议

```bash
# 备份所有数据库
mysqldump -u root -p --all-databases > all_databases_backup.sql

# 备份单个数据库
mysqldump -u root -p 数据库名 > backup.sql

# 定期备份（添加到 crontab）
0 2 * * * mysqldump -u root -p密码 数据库名 > /backup/db_$(date +\%Y\%m\%d).sql
```

---

## 📧 发送邮箱

收件人：120839976@qq.com  
主题：MySQL 密码重置指南（Mac）

---

**保存此文档，下次忘记密码时按步骤操作即可！** 🔐
