// One browser invocation: three desktop tops and three390px result views, offline route overlay.
const fs = require('node:fs/promises');
const path = require('node:path');
const {chromium} = require('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const O = __dirname;

(async () => {
  const inputs = JSON.parse(await fs.readFile(path.join(O, 'BUILD_INPUTS.json'), 'utf8'));
  const baseline = JSON.parse(await fs.readFile(path.join(O, 'BASELINE.json'), 'utf8'));
  const built = JSON.parse(await fs.readFile(path.join(O, 'BUILD.stdout.json'), 'utf8'));
  const files = new Map(baseline.public_file_pins.map(p => [p.path, path.join(baseline.website, p.path)]));
  for (const p of built.candidate_pins) files.set(p.path, path.join(O, 'candidate', p.path));
  const profile = path.join(O, 'render-profile');
  const output = path.join(O, 'renders');
  await fs.mkdir(output, {recursive: false});
  const context = await chromium.launchPersistentContext(profile, {
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true, serviceWorkers: 'block', acceptDownloads: false,
    viewport: {width: 1280, height: 1000},
    args: ['--disable-background-networking', '--disable-component-update', '--disable-sync', '--disable-breakpad', '--disable-crash-reporter', '--disk-cache-dir=' + path.join(profile, 'cache')]
  });
  const served = [], blocked = [], missing = [], consoleErrors = [], pageErrors = [], failed = [], views = [];
  await context.route('**/*', async route => {
    const request = route.request(), url = new URL(request.url());
    if (!/^https?:$/.test(url.protocol)) return route.continue();
    if (url.hostname !== 'private-stage.invalid' || request.method() !== 'GET') {
      blocked.push({url: url.href, method: request.method()});
      return route.abort();
    }
    let name = 'public' + decodeURIComponent(url.pathname);
    if (name.endsWith('/')) name += 'index.html';
    const source = files.get(name);
    if (!source) {
      missing.push(name);
      return route.fulfill({status: 404, body: 'Missing private overlay path'});
    }
    const type = name.endsWith('.html') ? 'text/html; charset=utf-8' : name.endsWith('.css') ? 'text/css' : name.endsWith('.pdf') ? 'application/pdf' : name.endsWith('.ico') ? 'image/x-icon' : 'application/octet-stream';
    served.push(name);
    return route.fulfill({status: 200, contentType: type, body: await fs.readFile(source)});
  });
  const page = context.pages()[0] || await context.newPage();
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => pageErrors.push(String(e)));
  page.on('requestfailed', r => failed.push({url: r.url(), error: r.failure()}));
  try {
    for (const article of inputs.articles) {
      await page.setViewportSize({width: 1280, height: 1000});
      await page.goto('https://private-stage.invalid/research/' + article.slug + '/', {waitUntil: 'load', timeout: 25000});
      await page.waitForTimeout(500);
      for (const [kind, width, height, id] of [['desktop-top', 1280, 1000, null], ['mobile-result', 390, 844, 'result']]) {
        await page.setViewportSize({width, height});
        await page.evaluate(id => window.scrollTo(0, id ? document.getElementById(id).getBoundingClientRect().top + window.scrollY - 12 : 0), id);
        const name = 'row' + article.row + '-' + kind;
        await page.screenshot({path: path.join(output, name + '.png'), timeout: 15000});
        views.push(await page.evaluate(name => ({name, viewport: window.innerWidth, documentWidth: document.documentElement.scrollWidth, scrollY: window.scrollY}), name));
      }
    }
    const result = {status: 'SIX_PRIVATE_PUBLIC_WRAPPER_VIEWS_SAVED', views, servedFromLocalOverlay: served, blockedExternalHTTP: blocked, missingOverlayPaths: missing, consoleErrors, pageErrors, requestFailures: failed, downloadClicks: 0, liveReaderOrDownloadCertification: false};
    await fs.writeFile(path.join(O, 'RENDER_RESULT.json'), JSON.stringify(result, null, 2) + '\n');
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  } finally {
    await context.close();
    await fs.rm(profile, {recursive: true, force: true});
  }
})().catch(error => { process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1; });
