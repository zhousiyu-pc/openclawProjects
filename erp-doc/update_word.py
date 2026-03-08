import re
import shutil

# 读取原始 markdown
with open('/home/admin/.openclaw/qqbot/downloads/日本跨境电商_ERP_系统_20260306_162933_1772786181736.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 mermaid 为高清图片引用
content = re.sub(
    r'```mermaid\ngraph TD.*?```',
    '\n\n![系统整体架构图](images/architecture_hd.png)\n\n',
    content, count=1, flags=re.DOTALL
)
content = re.sub(
    r'```mermaid\nflowchart TD.*?```',
    '\n\n![系统核心流程图](images/flowchart_hd.png)\n\n',
    content, count=1, flags=re.DOTALL
)

# 保存
with open('/home/admin/.openclaw/workspace/erp-doc/document_v2.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Markdown 已更新（高清图引用）")
