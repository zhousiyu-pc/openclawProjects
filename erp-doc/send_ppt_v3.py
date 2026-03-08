import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

to_email = "120839976@qq.com"
from_email = "120839976@qq.com"
password = "eaipoletwnfkbhfa"

msg = MIMEMultipart()
msg['From'] = "二狗子助手 <120839976@qq.com>"
msg['To'] = to_email
msg['Subject'] = "【PPT】日本跨境电商 ERP 合作伙伴演示文稿（14 页）"

body = """老板好！

这是给合作伙伴看的 PPT 演示文稿（第 3 次发送）。

📊 内容大纲（14 页）：
━━━━━━━━━━━━━━━━━━━━
1. 封面标题
2. 目录
3-4. 市场机会（20 万亿日元市场）
5-6. 产品定位（一句话说明白）
7-9. 15 大功能模块
10-11. ROI 分析（44 倍回报）
12-13. 投入与收益预测
14. 合作模式 + 联系方式
━━━━━━━━━━━━━━━━━━━━

📁 文件信息：
• 格式：Microsoft PowerPoint (.pptx)
• 大小：45KB
• 页数：14 页

💡 使用建议：
1. 电脑端打开效果最佳
2. 可直接投影演示
3. 每页都有演讲备注

如果还打不开，请截图告诉我具体显示什么！

---
二狗子 🐕
"""

msg.attach(MIMEText(body, 'utf-8'))

# 添加附件
file_path = "/home/admin/.openclaw/qqbot/downloads/partner_presentation.pptx"
with open(file_path, "rb") as f:
    attachment = f.read()
    
part = MIMEBase('application', 'vnd.openxmlformats-officedocument.presentationml.presentation')
part.set_payload(attachment)
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="日本跨境电商 ERP_合作伙伴演示.pptx"')
part.add_header('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation')
msg.attach(part)

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=90)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
    print("✅ PPT 已发送（第 3 次）")
except Exception as e:
    print(f"❌ 失败：{e}")
