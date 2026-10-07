import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

research = Path(__file__).resolve().parents[2]
review = Path(__file__).resolve().parent
package = review / 'extracted'
workspace = research.parent
checks = []

for relative, family in [('target_a/source_receipt.json', '197'),
                         ('target_b/source_receipts.json', '090')]:
    receipt = json.loads((package / relative).read_text())
    assert receipt.get('commit', receipt.get('upstream_commit')) == 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
    for entry in receipt['sources']:
        path = workspace / entry['local'] if family == '197' else research / 'target_b' / entry['path']
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert digest == entry['sha256'], str(path)
        assert blob == entry['git_blob_sha1'], str(path)
        if 'bytes' in entry:
            assert len(raw) == entry['bytes'], str(path)
        checks.append({'family': family, 'path': str(path.relative_to(workspace)),
                       'sha256': digest, 'git_blob_sha1': blob, 'bytes': len(raw)})

out = {'utc': datetime.now(timezone.utc).isoformat(),
       'status': 'PASS_ORIGINAL_SOURCE_IDENTITIES', 'count': len(checks),
       'pinned_commit': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a', 'checks': checks}
(review / 'ORIGINAL_SOURCE_IDENTITIES.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'count': out['count']}))
