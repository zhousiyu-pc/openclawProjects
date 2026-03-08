import re

with open('/home/admin/.openclaw/qqbot/downloads/日本跨境电商_ERP_系统_20260306_162933_1772786181736.md', 'r') as f:
    content = f.read()

# 提取所有mermaid代码块
mermaid_blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)

for i, block in enumerate(mermaid_blocks, 1):
    with open(f'/home/admin/.openclaw/workspace/erp-doc/diagram_{i}.mmd', 'w') as f:
        f.write(block)
    print(f'提取第{i}个图，共{len(block)}字符')

print(f'共提取{len(mermaid_blocks)}个mermaid图')
