# 检查 Word 文档中的图片
import zipfile
import os

doc_path = "/home/admin/.openclaw/qqbot/downloads/erp_requirements.docx"

# Word 文档本质是 ZIP 文件
with zipfile.ZipFile(doc_path, 'r') as zip_ref:
    # 列出所有文件
    files = zip_ref.namelist()
    print("文档内容：")
    for f in files:
        if 'image' in f.lower() or 'media' in f.lower():
            info = zip_ref.getinfo(f)
            print(f"  📷 {f} ({info.file_size} bytes)")
    
    # 检查文档 XML
    if 'word/document.xml' in files:
        content = zip_ref.read('word/document.xml').decode('utf-8', errors='ignore')
        if '<w:imagedata' in content or '<a:blip' in content:
            print("\n✅ 文档中有图片引用")
        else:
            print("\n❌ 文档中没有找到图片引用")
