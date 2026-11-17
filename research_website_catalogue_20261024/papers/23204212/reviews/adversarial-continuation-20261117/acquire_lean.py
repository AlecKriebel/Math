"""One HTTP request per actual pinned directory file; passive source acquisition."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent / 'primary'
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
items = json.loads((ROOT / 'lean-directory.json').read_text())
destination = ROOT / 'lean'
destination.mkdir(exist_ok=False)
for item in items:
    assert item['type'] == 'file' and item['name'].endswith('.lean')
    assert Path(item['name']).name == item['name']
    assert item['download_url'].startswith('https://raw.githubusercontent.com/openai/math/' + PIN + '/')

def transfer(item):
    receipt = {'UTC_start': datetime.now(timezone.utc).isoformat(), 'url': item['download_url'],
               'name': item['name'], 'expected_git_blob_sha1': item['sha'],
               'expected_bytes': item['size'], 'attempts': 1}
    try:
        with urllib.request.urlopen(item['download_url'], timeout=60) as response:
            data = response.read()
            receipt.update(status=response.status, headers=list(response.headers.items()),
                           final_url=response.url)
        (destination / item['name']).write_bytes(data)
        receipt.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                       git_blob_sha1=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest())
        assert receipt['bytes'] == item['size']
        assert receipt['git_blob_sha1'] == item['sha']
        receipt['success'] = True
    except Exception as error:
        receipt.update(success=False, error_type=type(error).__name__, error=str(error))
    receipt['UTC_end'] = datetime.now(timezone.utc).isoformat()
    (destination / (item['name'] + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt

with ThreadPoolExecutor(max_workers=4) as pool:
    receipts = list(pool.map(transfer, items))
(ROOT / 'LEAN_ACQUISITION.json').write_text(json.dumps(receipts, indent=2) + '\n')
print(json.dumps({'files': len(receipts), 'successes': sum(r['success'] for r in receipts),
                  'failures': [r for r in receipts if not r['success']]}, indent=2))
assert all(receipt['success'] for receipt in receipts), 'Acquisition failure retained; no retry'
