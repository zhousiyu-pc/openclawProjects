import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# 发件人配置（使用 QQ 邮箱 SMTP）
from_email = "openclaw@qq.com"  # 系统邮箱
to_email = "120839976@qq.com"
password = os.environ.get("QQ_MAIL_PASSWORD", "")  # 需要授权码

# 创建邮件
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "日本跨境电商 ERP 系统需求文档"

# 邮件正文
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

# 添加附件
file_path = "/home/admin/.openclaw/qqbot/downloads/erp_requirements.docx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="日本跨境电商 ERP 系统需求文档.docx"')
    msg.attach(part)

# 发送
try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=30)
    if password:
        server.login(from_email, password)
        server.send_message(msg)
        print("✅ 邮件发送成功！")
    else:
        print("⚠️ 缺少 QQ 邮箱授权码，无法发送")
        print("请在 QQ 邮箱设置中获取授权码，然后设置环境变量 QQ_MAIL_PASSWORD")
except Exception as e:
    print(f"❌ 发送失败：{e}")
