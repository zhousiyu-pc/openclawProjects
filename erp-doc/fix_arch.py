import re

# 读取原始架构图
with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1.mmd', 'r', encoding='utf-8') as f:
    content = f.read()

# 问题是subgraph中的中文可能被错误解析
# 让我把subgraph名称用引号包裹起来
# 修复: subgraph 用户层 -> subgraph "用户层"

def fix_subgraph(text):
    # 找到所有 subgraph 行并修复
    lines = text.split('\n')
    fixed_lines = []
    for line in lines:
        if 'subgraph' in line and 'end' not in line:
            # 提取subgraph名称
            match = re.match(r'(\s*subgraph\s+)(.+)', line)
            if match:
                prefix = match.group(1)
                name = match.group(2).strip()
                if not name.startswith('"'):
                    line = f'{prefix}"{name}"'
        fixed_lines.append(line)
    return '\n'.join(fixed_lines)

fixed_content = fix_subgraph(content)

with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("修复后的内容预览:")
print(fixed_content[:500])
