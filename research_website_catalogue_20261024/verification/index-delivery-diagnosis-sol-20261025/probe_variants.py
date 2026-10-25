"""Read-only follow-up checks suggested by actual ETags, Vary, and history."""
from probe_delivery import ROOT, PROGRAM, SITE, OUT, fetch, sha, now
import gzip
import json
import re
import subprocess

first = json.loads((ROOT / 'http-probe.json').read_text())
initial_path = PROGRAM / 'verification/research-index-freshness-20261025/initial-http.json'
prior = json.loads(initial_path.read_text())
old = prior['responses'][0]['headers']['etag']
old_date = prior['responses'][0]['headers']['last-modified']
current = dict((k.lower(), v) for k, v in first['requests'][0]['hops'][0]['headers'])['etag']
url = 'https://aleckriebel.com/research/'
cases = [
    ('conditional-current', url, {'If-None-Match': current}),
    ('conditional-prior44', url, {'If-None-Match': old}),
    ('conditional-prior44-no-cache', url, {'If-None-Match': old, 'Cache-Control': 'no-cache'}),
    ('modified-since-prior44', url, {'If-Modified-Since': old_date}),
    ('conditional-and-date-prior44', url, {'If-None-Match': old, 'If-Modified-Since': old_date}),
    ('gzip-ordinary', url, {'Accept-Encoding': 'gzip'}),
    ('gzip-no-cache', url, {'Accept-Encoding': 'gzip', 'Cache-Control': 'no-cache'}),
    ('article-referrer-navigation', url, {
        'Referer': 'https://aleckriebel.com/research/deep-derived-pure-braids-not-one-solvable/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1'}),
    ('firebase-default-host', 'https://aleckriebel-bd92e.web.app/research/', {}),
]
results = []
for label, u, headers in cases:
    item = fetch(label, u, headers)
    for hop in item['hops']:
        data = (ROOT / hop['body_file']).read_bytes()
        h = dict((k.lower(), v) for k, v in hop['headers'])
        if h.get('content-encoding') == 'gzip':
            decoded = gzip.decompress(data)
            path = hop['body_file'] + '.decoded'
            (ROOT / path).write_bytes(decoded)
            count = re.search(rb'"numberOfItems"\s*:\s*(\d+)', decoded)
            hop['decoded'] = {'bytes': len(decoded), 'sha256': sha(decoded), 'file': path,
                              'collection_number_of_items': int(count.group(1)) if count else None}
    results.append(item)
    (ROOT / 'variant-probe.json').write_text(json.dumps({
        'prior_validator_source': str(initial_path), 'prior_validator_source_sha256': sha(initial_path.read_bytes()),
        'prior44_etag': old, 'prior44_last_modified': old_date, 'current_etag': current,
        'requests': results}, indent=2) + '\n')
    final = item['hops'][-1]
    print(label, final['status'], final['bytes'], final.get('decoded', {}).get('sha256', final['sha256']),
          dict((k.lower(),v) for k,v in final['headers']).get('cache-control'),
          dict((k.lower(),v) for k,v in final['headers']).get('content-encoding'))

scan = subprocess.run(['rg', '-n', '-i', 'serviceWorker|service-worker|caches[.]open',
                       'public'], cwd=SITE, capture_output=True, text=True)
(ROOT / 'service-worker-source-scan.json').write_text(json.dumps({
    'utc': now(), 'command': ['rg','-n','-i','serviceWorker|service-worker|caches[.]open','public'],
    'exit_code': scan.returncode, 'stdout': scan.stdout, 'stderr': scan.stderr,
    'limitation': 'Source scan only; does not inspect browser registrations, extensions, or previously installed service workers.'
}, indent=2) + '\n')
