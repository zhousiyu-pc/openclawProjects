import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

from_email = "openclaw@qq.com"
to_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "日本跨境电商 ERP 系统需求文档"

body = """
老板好！

这是你要的日本跨境电商 ERP 系统需求文档，包含：

✅ 90 个功能点的详细设计
✅ 系统整体架构图（PNG）
✅ 核心业务流程图（PNG）
✅ 各模块接口定义、数据模型、测试用例

文档格式：Word (.docx)
文件大小：863KB

请查收！

---
二狗子 🐕
"""
msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/home/admin/.openclaw/qqbot/downloads/erp_requirements.docx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="日本跨境电商 ERP 系统需求文档.docx"')
    msg.attach(part)

# 重试 3 次
for i in range(3):
    try:
        print(f"尝试第 {i+1} 次发送...")
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ 邮件发送成功！已发送至 120839976@qq.com")
        break
    except Exception as e:
        print(f"第 {i+1} 次失败：{e}")
        if i < 2:
            time.sleep(3)
        else:
            print("❌ 3 次尝试均失败")
