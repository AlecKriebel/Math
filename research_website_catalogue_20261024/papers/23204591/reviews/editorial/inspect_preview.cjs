const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const here = __dirname;
  const out = path.join(here, 'preview-renders');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({executablePath: '/Users/alec/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing', headless: true, args: ['--disable-background-networking', '--disable-component-update', '--disable-sync', '--no-first-run']});
  const findings = [];
  try {
    for (const spec of [{name: 'desktop', width: 1280, height: 900}, {name: 'mobile', width: 390, height: 844}]) {
      const context = await browser.newContext({viewport: {width: spec.width, height: spec.height}, offline: true});
      const attemptedExternalRequests = [];
      await context.route(/^https?:/, route => { attemptedExternalRequests.push(route.request().url()); return route.abort(); });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.goto(pathToFileURL(path.join(here, 'preview.html')).href, {waitUntil: 'load'});
      await page.waitForTimeout(1200);
      await page.screenshot({path: path.join(out, spec.name + '-full.png'), fullPage: true});
      await page.screenshot({path: path.join(out, spec.name + '-top.png')});
      await page.locator('section:has(> h2#result)').screenshot({path: path.join(out, spec.name + '-result.png')});
      const state = await page.evaluate(() => ({
        title: document.title,
        width: innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        mainCount: document.querySelectorAll('main#main').length,
        h1Count: document.querySelectorAll('h1').length,
        bodyBackground: getComputedStyle(document.body).backgroundColor,
        fontFamily: getComputedStyle(document.body).fontFamily,
        robots: document.querySelector('meta[name=robots]').content,
        iframe: document.querySelector('iframe').getAttribute('src'),
        text: document.querySelector('main').innerText,
        links: [...document.querySelectorAll('main a')].map(a => ({text: a.innerText, href: a.getAttribute('href'), download: a.hasAttribute('download')})),
        elementsOutsideViewport: [...document.querySelectorAll('main *')].filter(e => {const r = e.getBoundingClientRect(); return r.left < -1 || r.right > innerWidth + 1;}).map(e => ({tag: e.tagName, text: e.innerText.slice(0, 160)}))
      }));
      findings.push({viewport: spec, state, attemptedExternalRequests, pageErrors: errors, networkScope: 'Offline file preview only; remote link destinations not fetched'});
      await context.close();
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(here, 'LAYOUT_INSPECTION.json'), JSON.stringify(findings, null, 2) + '\n');
  process.stdout.write(JSON.stringify({status: 'PRIVATE_OFFLINE_LAYOUT_CAPTURED', views: findings.map(x => ({name:x.viewport.name, horizontalOverflow:x.state.scrollWidth > x.state.width, pageErrors:x.pageErrors, attemptedExternalRequests:x.attemptedExternalRequests}))}, null, 2) + '\n');
})().catch(error => { process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1; });
