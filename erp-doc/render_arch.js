const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function render(file, out, w, h) {
    const code = fs.readFileSync(file, 'utf-8');
    const browser = await puppeteer.launch({
        executablePath: '/home/admin/.cache/puppeteer/chrome-headless-shell/linux-146.0.7680.31/chrome-headless-shell-linux64/chrome-headless-shell',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: w, height: h });
    const html = `<html><head><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script></head>
<body><div class="mermaid">${code}</div><script>mermaid.initialize({startOnLoad:true,theme:'default'})</script></body></html>`;
    await page.setContent(html, {waitUntil:'networkidle0',timeout:60000});
    await new Promise(r=>setTimeout(r,2000));
    await page.screenshot({path:out,fullPage:true});
    await browser.close();
    console.log('✅ '+out);
}

render('/home/admin/.openclaw/workspace/erp-doc/render_arch_simple.mmd', 
       '/home/admin/.openclaw/workspace/erp-doc/images/architecture_hd.png', 3600, 2400);
