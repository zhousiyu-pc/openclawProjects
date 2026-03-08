import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

# 尝试多个发件人配置
configs = [
    {"from": "noreply@qq.com", "smtp": "smtp.qq.com"},
]

to_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

msg = MIMEMultipart()
msg['From'] = "二狗子 <noreply@qq.com>"
msg['To'] = to_email
msg['Subject'] = "日本跨境电商 ERP 系统需求文档"

body = """老板好！

附件是日本跨境电商 ERP 系统需求文档（863KB），包含：
- 90 个功能点的详细设计
- 系统整体架构图
- 核心业务流程图
- 各模块接口定义、数据模型、测试用例

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
    part.add_header('Content-Disposition', 'attachment; filename="ERP_Demand.docx"')
    msg.attach(part)

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
    server.set_debuglevel(0)
    server.login("noreply@qq.com", password)
    server.send_message(msg)
    server.quit()
    print("✅ 邮件发送成功！")
except Exception as e:
    print(f"❌ 发送失败：{e}")
    print("\n建议：授权码可能不匹配发件人邮箱")
    print("请确认授权码是对应哪个 QQ 邮箱的")
