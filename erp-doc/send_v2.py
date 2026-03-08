import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

to_email = "120839976@qq.com"
from_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "日本跨境电商 ERP 系统需求文档（高清修订版）"

body = """老板好！

这是修订版需求文档，已修复：

✅ 系统架构图 - 高清重绘（3600x2400）
✅ 核心流程图 - 高清优化（4000x3000）
✅ 图片已嵌入 Word 文档

文档格式：Word (.docx)
文件大小：933KB

请查收！

---
二狗子 🐕
"""
msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/home/admin/.openclaw/qqbot/downloads/erp_requirements_v2.docx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="ERP_Demand_HD.docx"')
    msg.attach(part)

server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
server.login(from_email, password)
server.send_message(msg)
server.quit()
print("✅ 邮件发送成功！已发送至 120839976@qq.com")
