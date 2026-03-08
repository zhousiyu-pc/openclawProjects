import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys

# 获取进度参数
stage = sys.argv[1] if len(sys.argv) > 1 else "unknown"

to_email = "120839976@qq.com"
from_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

# 进度状态
progress = {
    "架构图": "✅",
    "流程图": "✅",
    "Word 更新": "🔄",
    "功能流程图": "🔄",
    "邮件发送": "⏳"
}

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "📊 ERP 文档进度汇报 - 二狗子"

body = f"""老板好！

这是定时进度汇报（每 5 分钟自动发送）

【当前进度】
✅ 架构图 HD - 已完成
✅ 流程图 HD - 已完成
🔄 Word 文档更新 - 进行中
🔄 功能流程图 - 设计中
⏳ 邮件发送 - 待处理

【预计完成时间】18:40

【下次汇报】5 分钟后

---
二狗子 🐕
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
    print("✅ 进度邮件已发送")
except Exception as e:
    print(f"❌ 发送失败：{e}")
