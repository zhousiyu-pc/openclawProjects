import requests
import base64
import zlib
import json

def mermaid_to_png_post(mermaid_code, output_file):
    """使用Kroki POST API转换mermaid图为PNG"""
    url = "https://kroki.io/mermaid/png"
    
    headers = {
        'Content-Type': 'text/plain'
    }
    
    try:
        response = requests.post(url, data=mermaid_code.encode('utf-8'), headers=headers, timeout=60)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"成功生成: {output_file} ({len(response.content)} bytes)")
            return True
        else:
            print(f"API返回错误: {response.status_code}")
            print(response.text[:500] if response.text else "No response")
            return False
    except Exception as e:
        print(f"转换失败: {e}")
        return False

with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1.mmd', 'r', encoding='utf-8') as f:
    diagram1 = f.read()

print("正在转换架构图...")
mermaid_to_png_post(diagram1, '/home/admin/.openclaw/workspace/erp-doc/images/architecture.png')
