import requests

with open('/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd', 'r', encoding='utf-8') as f:
    diagram = f.read()

url = "https://kroki.io/mermaid/png"
response = requests.post(url, data=diagram.encode('utf-8'), headers={'Content-Type': 'text/plain'}, timeout=60)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open('/home/admin/.openclaw/workspace/erp-doc/images/architecture.png', 'wb') as f:
        f.write(response.content)
    print(f"架构图成功! 大小: {len(response.content)} bytes")
else:
    print(f"Error: {response.text[:500]}")
