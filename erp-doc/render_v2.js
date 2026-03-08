const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function renderMermaid(mermaidCode, pngFile, width, height) {
    const browser = await puppeteer.launch({
        executablePath: '/home/admin/.cache/puppeteer/chrome-headless-shell/linux-146.0.7680.31/chrome-headless-shell-linux64/chrome-headless-shell',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: width, height: height });
    
    const html = `
<!DOCTYPE html>
<html>
<head><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>body { margin: 20px; background: white; }</style>
</head>
<body><div class="mermaid">${mermaidCode}</div>
<script>
mermaid.initialize({ startOnLoad: true, theme: 'default', securityLevel: 'loose', fontFamily: 'sans-serif' });
</script></body></html>`;
    
    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 90000 });
    await new Promise(r => setTimeout(r, 3000)); // 等待渲染完成
    await page.screenshot({ path: pngFile, fullPage: true });
    await browser.close();
    console.log(`✅ ${pngFile}`);
}

const arch = fs.readFileSync('/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd', 'utf-8');
const flow = fs.readFileSync('/home/admin/.openclaw/workspace/erp-doc/diagram_2.mmd', 'utf-8');

renderMermaid(arch, '/home/admin/.openclaw/workspace/erp-doc/images/architecture_hd.png', 4000, 3000)
    .catch(e => console.error('架构图失败:', e.message));

renderMermaid(flow, '/home/admin/.openclaw/workspace/erp-doc/images/flowchart_hd.png', 4000, 3000)
    .catch(e => console.error('流程图失败:', e.message));
