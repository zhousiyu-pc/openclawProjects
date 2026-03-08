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
msg['Subject'] = "日本跨境电商 ERP - 合作伙伴版 PPT"

body = """老板好！

这是给合作伙伴看的简化版 PPT，包含：

📋 6 大部分：
1. 项目背景与机会
2. 产品定位
3. 核心功能（15 大模块）
4. 商业价值（效率提升数据）
5. 投入与回报（ROI 分析）
6. 合作模式

📊 核心亮点：
- 效率提升 10 倍
- ROI 44 倍
- 投资回收期<1 年

文件格式：PPTX（45KB）
可直接用于演示！

---
二狗子 🐕
"""
msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/home/admin/.openclaw/qqbot/downloads/partner_presentation.pptx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="ERP_合作伙伴版 PPT.pptx"')
    msg.attach(part)

server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=60)
server.login(from_email, password)
server.send_message(msg)
server.quit()
print("✅ PPT 已发送至 120839976@qq.com")
