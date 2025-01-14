const puppeteer = require('puppeteer');
require('dotenv').config();

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
    await page.goto(process.env.ZABBIX_URL, { timeout: 90000 });

    // Isi username dan password
    console.log('Logging into Zabbix...');
    await page.type('input[name="name"]', process.env.ZABBIX_USERNAME);
    await page.type('input[name="password"]', process.env.ZABBIX_PASSWORD);
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
