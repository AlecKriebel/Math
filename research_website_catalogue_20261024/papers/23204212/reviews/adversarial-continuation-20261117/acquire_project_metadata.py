"""Passive one-request pinned project metadata and license acquisition."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent / 'primary'
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
names = {'LICENSE', 'lakefile.lean', 'lake-manifest.json', 'lean-toolchain', 'README.md'}
items = [i for i in json.loads((ROOT / 'project-directory.json').read_text()) if i['name'] in names]
assert {i['name'] for i in items} == names
receipts = []
for item in items:
    assert item['type'] == 'file'
    assert item['download_url'].startswith('https://raw.githubusercontent.com/openai/math/' + PIN + '/')
    target = ROOT / ('project-' + item['name'])
    assert not target.exists()
    receipt = {'UTC_start': datetime.now(timezone.utc).isoformat(), 'url': item['download_url'], 'attempts': 1}
    with urllib.request.urlopen(item['download_url'], timeout=60) as response:
        data = response.read()
        receipt.update(status=response.status, headers=list(response.headers.items()))
    target.write_bytes(data)
    receipt.update(name=target.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                   git_blob_sha1=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
                   expected_git_blob_sha1=item['sha'], UTC_end=datetime.now(timezone.utc).isoformat())
    (ROOT / (target.name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    assert len(data) == item['size'] and receipt['git_blob_sha1'] == item['sha']
    receipts.append(receipt)
(ROOT / 'PROJECT_ACQUISITION.json').write_text(json.dumps(receipts, indent=2) + '\n')
print(json.dumps({'successes': len(receipts), 'files': sorted(names)}))
