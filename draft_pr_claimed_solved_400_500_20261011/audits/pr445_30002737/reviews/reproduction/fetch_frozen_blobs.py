#!/usr/bin/env python3
"""Read-only verification of the receipt against exact GitHub commit blobs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
receipt = json.loads((CASE / 'SOURCE_RECEIPT.json').read_text())
head = receipt['head_sha']
private = HERE / 'private/frozen_remote'
private.mkdir(parents=True, exist_ok=True)
records = []
for item in receipt['files']:
    url = f'https://raw.githubusercontent.com/AlecKriebel/Math/{head}/' + item['path']
    record = {'path': item['path'], 'requested_url': url,
              'checked_at_utc': datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
            record['http_status'] = response.status
        observed_hash = hashlib.sha256(data).hexdigest()
        record.update(bytes=len(data), sha256=observed_hash,
                      matches_receipt=len(data) == item['bytes'] and observed_hash == item['sha256'])
        target = private / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if not record['matches_receipt']:
            raise ValueError('Remote frozen blob does not match receipt')
        record['status'] = 'verified'
    except Exception as exc:
        record.update(status='failed', error_type=type(exc).__name__, error=str(exc))
    records.append(record)
    print(item['path'], record['status'], flush=True)
result = {'frozen_head': head, 'files': records,
          'verified_count': sum(r['status'] == 'verified' for r in records),
          'failed_count': sum(r['status'] == 'failed' for r in records)}
(HERE / 'records/frozen_remote_provenance.json').write_text(json.dumps(result, indent=2)+'\n')
if result['failed_count']:
    raise RuntimeError('Not all frozen remote blobs verified; see raw records')
