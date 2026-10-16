"""Read-only exact-head binding check; outputs stay inside this review folder."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

HERE = Path(__file__).absolute().parent
AUDIT = HERE.parent.parent
ROOT = AUDIT.parents[2]
scope = json.loads((AUDIT / 'SCOPE_AND_SNAPSHOT.json').read_text())
head = scope['original_head']
rows = []
for rel, expected in scope['original_blobs'].items():
    local = (AUDIT / 'native' / rel).read_bytes()
    git = subprocess.run(['git', 'cat-file', 'blob', head + ':' + rel], cwd=ROOT,
                         check=True, capture_output=True).stdout
    git_oid = hashlib.sha1(b'blob ' + str(len(git)).encode() + b'\0' + git).hexdigest()
    row = {'path': rel, 'size': len(local), 'sha256': hashlib.sha256(local).hexdigest(),
           'git_blob': git_oid, 'local_matches_git': local == git}
    row['matches_snapshot'] = (row['size'] == expected['size'] and
                               row['sha256'] == expected['sha256'] and
                               row['git_blob'] == expected['git_blob'])
    rows.append(row)
result = {'utc': datetime.now(timezone.utc).isoformat(), 'head': head,
          'file_count': len(rows), 'all_pass': len(rows) == 24 and all(
              r['local_matches_git'] and r['matches_snapshot'] for r in rows),
          'files': rows}
(HERE / 'BINDING_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['utc', 'head', 'file_count', 'all_pass']}))
if not result['all_pass']:
    raise SystemExit(1)
