"""Bounded, read-only HTTP delivery probe; does not use a browser or client cache."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import hashlib
import http.client
import json
import re
import ssl
import subprocess

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT.parents[1]
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OUT = ROOT / 'raw'
OUT.mkdir(exist_ok=True)

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect(data):
    text = data.decode('utf-8', errors='replace')
    count = re.search(r'"numberOfItems"\s*:\s*(\d+)', text)
    return {
        'collection_number_of_items': int(count.group(1)) if count else None,
        'research_article_link_count': len(re.findall(r'<a\s+href="/research/[^/"]+/"', text)),
        'new_slugs_present': {slug: f'/research/{slug}/' in text for slug in [
            'deep-derived-pure-braids-not-one-solvable',
            'critical-wave-sparse-control-quadratic-growth',
            'generic-cantor-actions-wreath-product-hyperfinite']},
    }

def fetch(label, url, extra=None):
    # No request cache directives in ordinary mode; this client has no local cache.
    headers = {'User-Agent': 'Research index delivery diagnosis', 'Accept': '*/*',
               'Accept-Encoding': 'identity', 'Connection': 'close'}
    headers.update(extra or {})
    result = {'label': label, 'started_utc': now(), 'initial_url': url,
              'request_headers': headers, 'client': 'Python http.client, fresh TLS connection per hop; no local HTTP cache',
              'hops': []}
    for hop in range(5):
        parsed = urlsplit(url)
        path = parsed.path or '/'
        if parsed.query:
            path += '?' + parsed.query
        conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443,
                                            timeout=25, context=ssl.create_default_context())
        conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        data = response.read()
        received = now()
        hs = response.getheaders()
        filename = f'{label}-hop{hop}.body'
        (OUT / filename).write_bytes(data)
        item = {'url': url, 'status': response.status, 'reason': response.reason,
                'http_version': response.version, 'received_utc': received,
                'headers': hs, 'bytes': len(data), 'sha256': sha(data),
                'body_file': f'raw/{filename}', **inspect(data)}
        result['hops'].append(item)
        conn.close()
        location = dict((k.lower(), v) for k, v in hs).get('location')
        if response.status in (301, 302, 303, 307, 308) and location:
            url = urljoin(url, location)
        else:
            break
    result['finished_utc'] = now()
    return result

def main():
    sources = {}
    for rev in ['HEAD', '1ac93166', '4b19ea12']:
        for rel in ['public/research/index.html', 'firebase.json']:
            data = subprocess.check_output(['git', 'show', f'{rev}:{rel}'], cwd=SITE)
            sources[f'{rev}:{rel}'] = {'sha256': sha(data), 'bytes': len(data), **inspect(data)}
    for rel in ['firebase.json', '.firebaserc', 'README.md', 'deploy.sh',
                'public/research/index.html',
                'public/research/deep-derived-pure-braids-not-one-solvable/index.html']:
        data = (SITE / rel).read_bytes()
        (ROOT / ('local-' + rel.replace('/', '__'))).write_bytes(data)
    browsers = []
    browser_root = PROGRAM / 'verification/browser-braid-wave-cantor-sol-20261025'
    for name in ['index-initial-normal.json', 'index-one-normal-reload.json', 'index-desktop-return-braid.json']:
        data = (browser_root / name).read_bytes()
        d = json.loads(data)
        browsers.append({'file': str(browser_root / name), 'sha256': sha(data),
                         **{k: d.get(k) for k in ['url', 'utc', 'label', 'action', 'index_entry_count']},
                         'new_slugs_in_links': [link.get('raw_href') for link in d['links'] if any(
                             slug in link.get('raw_href', '') for slug in [
                                 'deep-derived-pure-braids', 'critical-wave-sparse', 'generic-cantor'])]})
    scope = {'started_utc': now(),
             'site_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SITE, text=True).strip(),
             'site_branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=SITE, text=True).strip(),
             'site_status_before': subprocess.check_output(['git', 'status', '--porcelain'], cwd=SITE, text=True),
             'source_revision_bindings': sources, 'browser_evidence_read_only': browsers,
             'scope': 'Only own diagnosis folder is written. No UI, browser APIs, site/source edits, deploy, settings changes, Git mutations, spreadsheet edits, or outreach.'}
    (ROOT / 'context.json').write_text(json.dumps(scope, indent=2) + '\n')
    routes = [
        ('index-canonical', 'https://aleckriebel.com/research/'),
        ('index-explicit', 'https://aleckriebel.com/research/index.html'),
        ('index-extensionless', 'https://aleckriebel.com/research'),
        ('braid-canonical', 'https://aleckriebel.com/research/deep-derived-pure-braids-not-one-solvable/'),
        ('braid-explicit', 'https://aleckriebel.com/research/deep-derived-pure-braids-not-one-solvable/index.html'),
        ('braid-extensionless', 'https://aleckriebel.com/research/deep-derived-pure-braids-not-one-solvable'),
    ]
    results = []
    for mode, hdr in [('ordinary', {}), ('no-cache', {'Cache-Control': 'no-cache'})]:
        for label, url in routes:
            results.append(fetch(label + '-' + mode, url, hdr))
            (ROOT / 'http-probe.json').write_text(json.dumps({'requests': results}, indent=2) + '\n')
    for item in results:
        print(item['label'], [(h['status'], h['bytes'], h['collection_number_of_items'],
                               dict((k.lower(),v) for k,v in h['headers']).get('cache-control'),
                               dict((k.lower(),v) for k,v in h['headers']).get('etag')) for h in item['hops']])

if __name__ == '__main__':
    main()
