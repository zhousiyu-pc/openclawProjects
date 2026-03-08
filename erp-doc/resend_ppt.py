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
msg['Subject'] = "【PPT 文件】日本跨境电商 ERP - 合作伙伴版（14 页）"

body = """老板好！

这是给合作伙伴看的 PPT 演示文稿，已重新发送。

📊 PPT 内容（14 页）：
1. 封面
2. 目录
3-4. 项目背景与机会
5-6. 产品定位
7-9. 核心功能（15 大模块）
10-11. 商业价值（ROI 分析）
12-13. 投入与回报
14. 合作模式 + 联系方式

📁 文件信息：
- 格式：PPTX（Microsoft PowerPoint）
- 大小：45KB
- 文件名：ERP_合作伙伴演示.pptx

⚠️ 如果还是打不开，可能是 QQ 邮箱附件显示问题，建议：
1. 电脑端登录 mail.qq.com 下载
2. 或者用 WPS/Office 打开

---
二狗子 🐕
"""
msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/home/admin/.openclaw/qqbot/downloads/partner_presentation.pptx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'application/vnd.openxmlformats-officedocument.presentationml.presentation')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="ERP_合作伙伴演示.pptx"')
    msg.attach(part)

server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
server.login(from_email, password)
server.send_message(msg)
server.quit()
print("✅ PPT 已重新发送至 120839976@qq.com")
