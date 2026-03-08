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
msg['Subject'] = "【PPT】日本跨境电商 ERP 合作伙伴演示（14 页）"

body = """老板好！

这是给合作伙伴看的 PPT 演示文稿。

📊 内容（14 页）：
1. 封面
2. 目录
3-4. 市场机会
5-6. 产品定位
7-9. 15 大功能模块
10-11. ROI 分析（44 倍）
12-13. 投入收益
14. 合作模式

📁 文件：日本跨境电商 ERP_合作伙伴演示.pptx (45KB)

---
二狗子
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/home/admin/.openclaw/qqbot/downloads/partner_presentation.pptx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="ERP_Partner_Presentation.pptx"')
    msg.attach(part)

server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=90)
server.login(from_email, password)
server.send_message(msg)
server.quit()
print("✅ 已发送")
