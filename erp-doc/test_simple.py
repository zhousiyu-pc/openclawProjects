import requests

# 测试一个简单的mermaid图
simple_mermaid = """graph TD
    A[开始] --> B[结束]
"""

url = "https://kroki.io/mermaid/png"
response = requests.post(url, data=simple_mermaid.encode('utf-8'), headers={'Content-Type': 'text/plain'}, timeout=30)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open('/home/admin/.openclaw/workspace/erp-doc/images/test.png', 'wb') as f:
        f.write(response.content)
    print("简单图测试成功!")
else:
    print(response.text[:200])
