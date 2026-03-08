const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function renderMermaid(mmdFile, pngFile) {
    const mermaidCode = fs.readFileSync(mmdFile, 'utf-8');
    
    const browser = await puppeteer.launch({
        executablePath: '/home/admin/.cache/puppeteer/chrome-headless-shell/linux-146.0.7680.31/chrome-headless-shell-linux64/chrome-headless-shell',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 2400, height: 1800 });
    
    const html = `
<!DOCTYPE html>
<html>
<head><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script></head>
<body>
<div class="mermaid">${mermaidCode}</div>
<script>
mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>
</body>
</html>`;
    
    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 60000 });
    await page.waitForSelector('.mermaid svg', { timeout: 30000 });
    await page.screenshot({ path: pngFile, fullPage: true });
    
    await browser.close();
    console.log(`✅ 成功：${pngFile}`);
}

renderMermaid(
    '/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd',
    '/home/admin/.openclaw/workspace/erp-doc/images/architecture.png'
).catch(err => console.error('❌ 失败:', err.message));
