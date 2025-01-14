const puppeteer = require('puppeteer');

(async () => {
  const args = process.argv.slice(2);
  const graphUrl = args[0];
  const output = args[1];

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
  const page = await browser.newPage();

  try {
    // Atur viewport ke ukuran tertentu
    await page.setViewport({ width: 1500, height: 800 });

    // Akses halaman login Zabbix
    console.log('Accessing Zabbix login page...');
    await page.goto("http://10.8.8.65/zabbix", { timeout: 90000 });

    // Isi username dan password
    console.log('Logging into Zabbix...');
    await page.type('input[name="name"]', 'Admin');
    await page.type('input[name="password"]', 'pr@w4th1y4');
    await page.click('button[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });

    console.log('Login successful. Waiting for page to load...');
    await new Promise((resolve) => setTimeout(resolve, 6000));

    console.log('Navigating to graph URL...');
   
    await page.goto(graphUrl, { timeout: 90000, waitUntil: 'networkidle2' });

    
    await page.screenshot({
      path: output,
      fullPage: true,
    });

    console.log(`Screenshot saved to ${output}`);
  } catch (error) {
    console.error('Error capturing screenshot:', error);
  } finally {
    await browser.close();
  }
})();
