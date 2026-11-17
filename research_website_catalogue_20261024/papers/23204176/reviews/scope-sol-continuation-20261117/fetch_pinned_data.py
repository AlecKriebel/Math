"""Read-only HTTPS retrieval of explicitly listed pinned primary source bytes."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/scope-sol-continuation-20261117')
NATIVE = OWN.parent.parent / 'sources/archives/01-source-and-verification.zip.extracted/UPSTREAM_MANIFEST.json'
manifest_bytes = NATIVE.read_bytes()
manifest = json.loads(manifest_bytes)
commit = manifest['pinned_commit']
assert commit == 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
assert not (OWN / 'primary').exists()
(OWN / 'primary').mkdir()
(OWN / 'PINNED_RETRIEVAL_INPUT.json').write_bytes(manifest_bytes)


def fetch(row):
    rel = row['path']
    assert not rel.startswith('/') and '..' not in Path(rel).parts
    path = OWN / 'primary' / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists()
    url = 'https://raw.githubusercontent.com/openai/math/' + commit + '/' + rel
    result = {'path': rel, 'URL': url, 'started_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'attempts': 1}
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
            result.update(status=response.status, final_URL=response.url, headers=dict(response.headers))
        path.write_bytes(data)
        actual = hashlib.sha256(data).hexdigest()
        result.update(bytes=len(data), sha256=actual, matches_published_pin=(len(data) == row['bytes'] and actual == row['sha256']))
    except Exception as error:
        result.update(error_type=type(error).__name__, error=str(error), matches_published_pin=False)
    result['finished_UTC'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return result


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, manifest['files']))
output = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'commit': commit,
          'input_sha256': hashlib.sha256(manifest_bytes).hexdigest(), 'files': results,
          'all_exact': all(r['matches_published_pin'] for r in results), 'network_mutations': False}
(OWN / 'PINNED_RETRIEVAL.json').write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
print(json.dumps({'files': len(results), 'all_exact': output['all_exact'], 'failed': [r['path'] for r in results if not r['matches_published_pin']]}))
