const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function renderHD(mmdFile, pngFile, width, height) {
    const mermaidCode = fs.readFileSync(mmdFile, 'utf-8');
    
    const browser = await puppeteer.launch({
        executablePath: '/home/admin/.cache/puppeteer/chrome-headless-shell/linux-146.0.7680.31/chrome-headless-shell-linux64/chrome-headless-shell',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: width, height: height });
    
    const html = `
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
body { font-family: "Microsoft YaHei", sans-serif; margin: 40px; }
.mermaid { font-size: 18px; }
</style>
</head>
<body>
<div class="mermaid">${mermaidCode}</div>
<script>
mermaid.initialize({ 
    startOnLoad: true, 
    theme: 'default',
    fontFamily: 'Microsoft YaHei',
    fontSize: 16,
    flowchart: { useMaxWidth: false, htmlLabels: true }
});
</script>
</body>
</html>`;
    
    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 60000 });
    await page.waitForSelector('.mermaid svg', { timeout: 30000 });
    
    // 截图
    await page.screenshot({ path: pngFile, fullPage: true });
    
    await browser.close();
    console.log(`✅ ${pngFile}`);
}

// 渲染高清图
Promise.all([
    renderHD('/home/admin/.openclaw/workspace/erp-doc/diagram_1_fixed.mmd', 
             '/home/admin/.openclaw/workspace/erp-doc/images/architecture_hd.png', 3200, 2400),
    renderHD('/home/admin/.openclaw/workspace/erp-doc/diagram_2.mmd', 
             '/home/admin/.openclaw/workspace/erp-doc/images/flowchart_hd.png', 3200, 2400)
]).catch(err => console.error('❌', err.message));
