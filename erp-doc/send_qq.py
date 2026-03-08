import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

# 发件人：120839976@qq.com (收件人自己的邮箱)
from_email = "120839976@qq.com"
to_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "日本跨境电商 ERP 系统需求文档"

body = """这是你要的日本跨境电商 ERP 系统需求文档。

包含：
- 90 个功能点的详细设计
- 系统整体架构图
- 核心业务流程图
- 各模块接口定义、数据模型、测试用例

文档格式：Word (.docx)
文件大小：863KB

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

for i in range(5):
    try:
        print(f"第 {i+1} 次尝试...")
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=90)
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("\n✅ 邮件发送成功！已发送至 120839976@qq.com")
        break
    except Exception as e:
        print(f"失败：{e}")
        if i < 4:
            time.sleep(5)
        else:
            print("\n❌ 5 次尝试均失败")
            print("\n可能原因：")
            print("1. 授权码不对（授权码≠QQ 密码，需在邮箱设置中获取）")
            print("2. 发件人邮箱不是 120839976@qq.com")
            print("3. 网络问题")
