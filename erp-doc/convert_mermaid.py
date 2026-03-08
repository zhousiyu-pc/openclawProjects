import requests
import base64
import json
import zlib

def mermaid_to_png(mermaid_code, output_file):
    """使用mermaid.ink API转换mermaid图为PNG"""
    # 压缩并编码
    compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    url = f"https://mermaid.ink/img/{encoded}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"成功生成: {output_file}")
            return True
        else:
            print(f"API返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"转换失败: {e}")
        return False

# 转换两个图
with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1.mmd', 'r') as f:
    diagram1 = f.read()

with open('/home/admin/.openclaw/workspace/erp-doc/diagram_2.mmd', 'r') as f:
    diagram2 = f.read()

mermaid_to_png(diagram1, '/home/admin/.openclaw/workspace/erp-doc/images/architecture.png')
mermaid_to_png(diagram2, '/home/admin/.openclaw/workspace/erp-doc/images/flowchart.png')
