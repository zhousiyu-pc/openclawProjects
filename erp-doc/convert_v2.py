import requests
import base64
import zlib

with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd', 'r', encoding='utf-8') as f:
    diagram = f.read()

# 方法1: 使用base64编码
encoded = base64.urlsafe_b64encode(diagram.encode('utf-8')).decode('ascii')
url = f"https://kroki.io/mermaid/png/{encoded}"

response = requests.get(url, timeout=60)
print(f"Method 1 Status: {response.status_code}")
if response.status_code == 200:
    with open('/home/admin/.openclaw/workspace/erp-doc/images/architecture.png', 'wb') as f:
        f.write(response.content)
    print(f"架构图成功! 大小: {len(response.content)} bytes")
else:
    print(f"Error: {response.text[:300]}")
