"""Verify deployed research pages and unchanged assets against this checkout."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
ids = [str(int(value)) for value in sys.argv[1:]]
assert ids
paths = ['research/index.html', 'research/research.css', 'research/sitemap.xml']
for rid in ids:
    c = json.loads((ROOT/'papers'/rid/'publication.json').read_text())
    names = ['index.html', 'citation.bib', c['pdf_filename']]
    if c.get('supplement_filename'): names.append(c['supplement_filename'])
    names += [asset['filename'] for asset in c.get('additional_assets', [])]
    paths += [f'research/{c["slug"]}/{name}' for name in names]

def check(path):
    url = 'https://aleckriebel.com/' + (path[:-10] if path.endswith('index.html') else path)
    expected = hashlib.sha256((PUBLIC/path).read_bytes()).hexdigest()
    with urlopen(Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Research publication verification'}), timeout=45) as response:
        data = response.read()
        actual = hashlib.sha256(data).hexdigest()
        result = {'path': path, 'url': url, 'resolved_url': response.url,
                  'status': response.status, 'content_type': response.headers.get('Content-Type'),
                  'bytes': len(data), 'expected_sha256': expected, 'actual_sha256': actual,
                  'passed': response.status == 200 and actual == expected}
    return result

results = list(ThreadPoolExecutor(max_workers=4).map(check, paths))
receipt = {'verified_utc': datetime.now(timezone.utc).isoformat(), 'records': ids,
           'passed': all(item['passed'] for item in results), 'checks': results}
output = ROOT/'verification'/('live-'+'-'.join(ids)+'.json')
output.write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({'receipt': str(output), 'passed': receipt['passed'], 'files_checked': len(results)}))
if not receipt['passed']:
    raise SystemExit(1)
