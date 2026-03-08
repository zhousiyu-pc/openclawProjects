import re

# 读取原始 markdown
with open('/home/admin/.openclaw/qqbot/downloads/日本跨境电商_ERP_系统_20260306_162933_1772786181736.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换第一个 mermaid 块为架构图
content = re.sub(
    r'```mermaid\ngraph TD.*?```',
    '![系统整体架构图](images/architecture.png)',
    content,
    count=1,
    flags=re.DOTALL
)

# 替换第二个 mermaid 块为流程图
content = re.sub(
    r'```mermaid\nflowchart TD.*?```',
    '![系统核心流程图](images/flowchart.png)',
    content,
    count=1,
    flags=re.DOTALL
)

# 保存修改后的 markdown
with open('/home/admin/.openclaw/workspace/erp-doc/document_for_word.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Markdown 已准备好，mermaid 代码块已替换为图片引用")
