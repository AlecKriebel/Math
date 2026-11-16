// One offline browser invocation, six saved views, no clicks or downloads.
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const O = __dirname;

(async () => {
  const output = path.join(O, 'renders');
  const profile = path.join(O, 'render-profile');
  await fs.mkdir(output, {recursive: false});
  const context = await chromium.launchPersistentContext(profile, {
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    serviceWorkers: 'block',
    acceptDownloads: false,
    viewport: {width: 1280, height: 900},
    args: ['--allow-file-access-from-files', '--disable-background-networking', '--disable-component-update', '--disable-sync', '--disable-breakpad', '--disable-crash-reporter', '--disk-cache-dir=' + path.join(profile, 'cache')]
  });
  const blocked = [], requests = [], failed = [], consoleErrors = [], pageErrors = [], views = [];
  await context.route('**/*', async route => {
    const url = route.request().url();
    if (/^https?:/i.test(url)) {
      blocked.push(url);
      await route.abort();
    } else {
      await route.continue();
    }
  });
  const page = context.pages()[0] || await context.newPage();
  page.on('request', r => requests.push(r.url()));
  page.on('requestfailed', r => failed.push({url: r.url(), error: r.failure()}));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => pageErrors.push(String(e)));
  try {
    await page.goto(pathToFileURL(path.join(O, 'preview/index.html')).href, {waitUntil: 'load', timeout: 25000});
    await page.waitForTimeout(700);
    for (const [name, width, height, id] of [
      ['desktop-top', 1280, 900, null],
      ['desktop-result', 1280, 900, 'result'],
      ['desktop-downloads', 1280, 900, 'downloads'],
      ['mobile-top', 390, 844, null],
      ['mobile-explanation', 390, 844, 'explanation'],
      ['mobile-abstract', 390, 844, 'original-abstract']
    ]) {
      await page.setViewportSize({width, height});
      await page.evaluate(id => window.scrollTo(0, id ? document.getElementById(id).getBoundingClientRect().top + window.scrollY - 20 : 0), id);
      await page.screenshot({path: path.join(output, name + '.png'), timeout: 15000});
      views.push(await page.evaluate(name => ({name, viewport: window.innerWidth, documentWidth: document.documentElement.scrollWidth, scrollY: window.scrollY, iframe: {width: document.querySelector('iframe').clientWidth, height: document.querySelector('iframe').clientHeight}}), name));
    }
    const result = {status: 'SIX_OFFLINE_VIEWS_SAVED', views, blockedHTTP: blocked, pageRequests: requests, requestFailures: failed, consoleErrors, pageErrors, downloadClicks: 0, nativePDFOrLiveDownloadCertification: false};
    await fs.writeFile(path.join(O, 'RENDER_RESULT.json'), JSON.stringify(result, null, 2) + '\n');
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  } finally {
    await context.close();
    await fs.rm(profile, {recursive: true, force: true});
  }
})().catch(error => { process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1; });
