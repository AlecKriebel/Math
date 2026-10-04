"""Private candidate replay after independence seal; all public streams are JSON.

The candidate is copied under this auditor's ignored tmp directory. No author,
snapshot, repository-index, Git-service, or source-PDF mutation is performed.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import time

p = Path(__file__).resolve().parent
audit = p.parent
snapshot = audit/'snapshot'
manifest = json.loads((audit/'snapshot_manifest.json').read_text())
assert manifest['head'] == '36c29bb039471f132889d577c9322d78925b62dd'
objects = []
for e in manifest['files']:
    data = (snapshot/e['path']).read_bytes()
    assert len(data) == e['bytes']
    assert hashlib.sha256(data).hexdigest() == e['sha256']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == e['git_blob_sha']
    objects.append({'path':e['path'], 'sha256':e['sha256'], 'git_blob_sha':e['git_blob_sha']})
assert len(objects) == 54
src = snapshot/'unsolved_math_prioritization/attempts/30004293'
dest = p/'tmp/candidate'
assert not dest.exists()
shutil.copytree(src, dest)

bindings = []
for name in sorted(dest.glob('*MANIFEST.json')):
    obj = json.loads(name.read_text())
    for e in obj.get('files', []):
        f = dest/e['path']
        data = f.read_bytes()
        assert len(data) == e['bytes'] and hashlib.sha256(data).hexdigest() == e['sha256']
        bindings.append({'manifest':name.name, 'path':e['path'], 'sha256':e['sha256']})
for e in json.loads((dest/'review/REVIEW_MANIFEST.json').read_text())['files']:
    data = (dest/'review'/e['path']).read_bytes()
    assert len(data) == e['bytes'] and hashlib.sha256(data).hexdigest() == e['sha256']
    bindings.append({'manifest':'review/REVIEW_MANIFEST.json', 'path':e['path'], 'sha256':e['sha256']})
for e in json.loads((dest/'review/REMOTE_BINDING.json').read_text())['files']:
    data = (dest/e['path']).read_bytes()
    assert len(data) == e['size']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == e['sha']

results = []
jobs = [(f'author_turn_{i}', dest/f'verify_turn{i}.py', dest/f'TURN_{i}_CHECKS.json')
        for i in range(1, 6)]
jobs.append(('historical_independent', dest/'review/independent_checks.py', dest/'review/INDEPENDENT_CHECKS.json'))
for label, script, expected in jobs:
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    run = subprocess.run([sys.executable, str(script)], cwd=dest,
                         capture_output=True, timeout=180)
    (p/f'{label}.stdout').write_bytes(run.stdout)
    (p/f'{label}.stderr').write_bytes(run.stderr)
    item = {'label':label, 'utc_started':started, 'seconds':time.monotonic()-tick,
            'exit_code':run.returncode, 'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),
            'stderr_sha256':hashlib.sha256(run.stderr).hexdigest(),
            'receipt_byte_exact':run.stdout == expected.read_bytes()}
    assert run.returncode == 0 and item['receipt_byte_exact'], item
    item['receipt'] = json.loads(run.stdout)
    results.append(item)
    print(json.dumps(item), flush=True)

out = {'utc':datetime.now(timezone.utc).isoformat(), 'frozen_original_head':manifest['head'],
       'snapshot_objects_verified':len(objects), 'target_objects_verified':53,
       'all_manifest_entries_verified':len(bindings), 'source_pdfs_replayed':False,
       'source_pdf_limitation':'Only the auditor three primary inputs were retrieved; five-author-source collection was not replayed',
       'runtime':sys.version, 'private_candidate_directory':'tmp/candidate',
       'independence_seal_precedes_candidate_read':True, 'jobs':results,
       'snapshot_objects':objects, 'manifest_bindings':bindings}
(p/'PRIVATE_REPLAY.json').write_text(json.dumps(out, indent=2)+'\n')
