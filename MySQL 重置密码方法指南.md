# MySQL 重置密码方法 - 完整指南

## 📋 方法一：使用 --skip-grant-tables（推荐）

### 步骤 1：停止 MySQL 服务
```bash
sudo systemctl stop mysql
# 或
sudo service mysql stop
```

### 步骤 2：以安全模式启动 MySQL
```bash
sudo mysqld_safe --skip-grant-tables --skip-networking &
```

### 步骤 3：无密码登录 MySQL
```bash
mysql -u root
```

### 步骤 4：重置密码
```sql
-- 刷新权限
FLUSH PRIVILEGES;

-- 修改密码（MySQL 5.7+）
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';

-- 或（MySQL 5.6 及以下）
UPDATE mysql.user SET Password=PASSWORD('新密码') WHERE User='root';
FLUSH PRIVILEGES;
```

### 步骤 5：重启 MySQL 服务
```bash
# 先停止安全模式
sudo mysqladmin -u root shutdown

# 正常启动
sudo systemctl start mysql
```

---

## 📋 方法二：使用 --init-file

### 步骤 1：创建密码重置文件
```bash
sudo nano /tmp/mysql-reset.sql
```

### 步骤 2：写入重置密码 SQL
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
FLUSH PRIVILEGES;
```

### 步骤 3：停止 MySQL 服务
```bash
sudo systemctl stop mysql
```

### 步骤 4：使用初始化文件启动
```bash
sudo mysqld_safe --init-file=/tmp/mysql-reset.sql &
```

### 步骤 5：重启正常服务
```bash
sudo systemctl restart mysql
sudo rm /tmp/mysql-reset.sql
```

---

## 📋 方法三：使用 mysqladmin 命令

### 适用于已知旧密码的情况
```bash
mysqladmin -u root -p password '新密码'
# 输入旧密码后，密码即被修改
```

---

## 📋 方法四：Docker 环境重置密码

### 步骤 1：进入容器
```bash
docker exec -it mysql_container bash
```

### 步骤 2：在容器内执行
```bash
mysql -u root <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
FLUSH PRIVILEGES;
EOF
```

---

## 🔐 密码安全建议

| 要求 | 说明 |
|------|------|
| **长度** | ≥12 位 |
| **复杂度** | 大小写字母 + 数字 + 特殊符号 |
| **定期更换** | 每 90 天 |
| **不要复用** | 不同服务使用不同密码 |

### 生成强密码示例
```bash
# 生成 16 位随机密码
openssl rand -base64 16

# 或使用
cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%' | fold -w 16 | head -n 1
```

---

## ⚠️ 常见问题

### Q1: 忘记 root 密码且无法停止 MySQL？
```bash
# 尝试强制停止
sudo killall -9 mysqld
sudo systemctl stop mysql
```

### Q2: 重置后无法登录？
```bash
# 检查密码是否包含特殊字符需要转义
mysql -u root -p'密码'  # 注意引号
```

### Q3: 远程连接被拒绝？
```sql
-- 允许远程连接
CREATE USER 'root'@'%' IDENTIFIED BY '密码';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

---

## 📊 各版本命令对比

| MySQL 版本 | 重置密码命令 |
|-----------|-------------|
| **8.0+** | `ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';` |
| **5.7** | `ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';` |
| **5.6 及以下** | `UPDATE mysql.user SET Password=PASSWORD('新密码') WHERE User='root';` |

---

## 📝 完整操作记录模板

```bash
# 记录操作时间
date: 2026-03-07

# 1. 停止服务
sudo systemctl stop mysql

# 2. 安全模式启动
sudo mysqld_safe --skip-grant-tables --skip-networking &

# 3. 登录并重置
mysql -u root
> FLUSH PRIVILEGES;
> ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
> EXIT;

# 4. 重启服务
sudo mysqladmin -u root shutdown
sudo systemctl start mysql

# 5. 验证登录
mysql -u root -p'新密码'
```

---

## 📞 文档信息

- **版本**：1.0
- **整理**：二狗子 🐕
- **日期**：2026 年 3 月 7 日
- **适用系统**：Linux (Ubuntu/CentOS/Debian)
- **适用版本**：MySQL 5.6 / 5.7 / 8.0+

---

**⚠️ 重要提醒：**
1. 重置密码后请立即修改为强密码
2. 删除临时的 SQL 文件（如 /tmp/mysql-reset.sql）
3. 检查 MySQL 日志确认无异常（/var/log/mysql/error.log）
4. 建议配置密码过期策略和登录失败锁定
