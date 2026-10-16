#!/usr/bin/env python3
"""Read-only remote/snapshot bindings and isolated diagnostic replays.

Writes receipts only to this audit directory, and foreign/download/run data to
ignored tmp. Does not execute Git, edit the PR or any canonical queue state.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import shutil
import sqlite3
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[2]
TMP = HERE/'tmp'
CANDIDATE = AUDIT/'reviewed_candidate'
SNAPSHOT = AUDIT/'source_snapshot'
HEAD = '5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def frozen_inventory():
    manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
    assert manifest['head'] == HEAD
    records = []
    for m in manifest['files']:
        local = (SNAPSHOT/m['path']).read_bytes()
        assert sha(local) == m['sha256'] and len(local) == m['bytes']
        blob = hashlib.sha1(b'blob '+str(len(local)).encode()+b'\0'+local).hexdigest()
        assert blob == m['git_blob']
        url = 'https://raw.githubusercontent.com/AlecKriebel/Math/'+HEAD+'/unsolved_math_prioritization/attempts/20002011/'+m['path']
        with urllib.request.urlopen(url, timeout=30) as r:
            remote = r.read()
        dest = TMP/'remote_exact_head'/m['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(remote)
        assert remote == local
        records.append({'path': m['path'], 'bytes': len(local), 'sha256': sha(local),
                        'git_blob_sha1': blob, 'independent_raw_exact_head_byte_equal': True})
    return records


def current_inventory():
    manifest = json.loads((CANDIDATE/'MANIFEST.json').read_text())
    records = []
    for name, expected in manifest['sha256'].items():
        b = (CANDIDATE/name).read_bytes()
        assert sha(b) == expected
        records.append({'path': name, 'bytes': len(b), 'sha256': sha(b)})
    assert len(records) == 19
    names = {str(p.relative_to(CANDIDATE)) for p in CANDIDATE.rglob('*') if p.is_file()}
    assert names == set(manifest['sha256'])|{'MANIFEST.json'}
    old, new = (SNAPSHOT/'SOURCE_STATUS.md').read_bytes(), (CANDIDATE/'SOURCE_STATUS.md').read_bytes()
    assert old[old.index(b'## 1.'): ] == new[new.index(b'## 1.'): ]
    assert (CANDIDATE/'ORIGINAL_PROVENANCE.json').read_bytes() == (SNAPSHOT/'provenance.json').read_bytes()
    assert (CANDIDATE/'ORIGINAL_READINESS.json').read_bytes() == (SNAPSHOT/'readiness.json').read_bytes()
    unchanged = []
    for p in SNAPSHOT.rglob('*'):
        if p.is_file():
            name = str(p.relative_to(SNAPSHOT))
            if (CANDIDATE/name).read_bytes() == p.read_bytes():
                unchanged.append(name)
    db = sqlite3.connect('file:'+str(ROOT/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro', uri=True)
    pinned = []
    for id, name in [(20002011, 'source_record.json'), (20002052, 'duplicate_source_record.json')]:
        row = db.execute('SELECT payload,report FROM records WHERE key=?',(str(id),)).fetchone()
        p, r = json.loads(row[0]), json.loads(row[1])
        assert p == json.loads((CANDIDATE/name).read_text())
        pinned.append({'id': id, 'problem_source_equal': True,
                       'canonical_problem_json_sha256': sha(json.dumps(p,sort_keys=True).encode()),
                       'canonical_prior_json_sha256': sha(json.dumps(r,sort_keys=True).encode()),
                       'review_hash': sha(json.dumps([p,r],sort_keys=True).encode()),
                       'full_prior_report_fields': sorted(r)})
    return {'manifest_sha256': sha((CANDIDATE/'MANIFEST.json').read_bytes()),
            'files': records, 'unchanged_original_files': unchanged,
            'mathematics_sections_1_onward_byte_unchanged': True,
            'original_provenance_and_readiness_preserved': True, 'pinned_records': pinned}


def replay(name, src, script, output, expected=None):
    dest = TMP/'diagnostic_replays'/name
    assert not dest.exists(), 'Preserve earlier runs; choose a fresh name'
    if src.is_dir():
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('tmp'))
    else:
        dest.mkdir(parents=True)
        shutil.copy2(src, dest/script)
    proc = subprocess.run(['/usr/bin/python3', str(dest/script)], cwd=dest,
                          capture_output=True, timeout=240)
    (dest/'stdout.txt').write_bytes(proc.stdout)
    (dest/'stderr.txt').write_bytes(proc.stderr)
    assert proc.returncode == 0, proc.stderr.decode()
    b = (dest/output).read_bytes()
    parsed = json.loads(b)
    equal = None
    if expected is not None:
        equal = b == expected.read_bytes()
        assert equal
    return {'name': name, 'script': script, 'script_sha256': sha((dest/script).read_bytes()),
            'receipt': output, 'receipt_sha256': sha(b), 'byte_identical_to_saved_receipt': equal,
            'exit_code': proc.returncode, 'sympy_version': parsed['sympy_version'],
            'assertions': parsed.get('passed', parsed.get('exact_assertions',parsed.get('assertions'))),
            'stdout_sha256': sha(proc.stdout), 'stderr_empty': not proc.stderr}


current = current_inventory()
frozen = frozen_inventory()
jobs = [
    ('author_original', SNAPSHOT, 'check_jets.py', 'check_results.json', SNAPSHOT/'check_results.json'),
    ('historical_independent', SNAPSHOT, 'independent_review/independent_checks.py',
     'independent_review/independent_results.json', SNAPSHOT/'independent_review/independent_results.json'),
    ('new_variational_family', AUDIT/'variational_family', 'fresh_variational_controls.py',
     'FRESH_CONTROL_RESULTS.json', AUDIT/'variational_family/FRESH_CONTROL_RESULTS.json'),
    ('new_geometric_family', AUDIT/'geometric_family', 'fresh_geometric_controls.py',
     'FRESH_GEOMETRIC_RESULTS.json', AUDIT/'geometric_family/FRESH_GEOMETRIC_RESULTS.json'),
    ('fresh_periodic', HERE/'fresh_periodic_controls.py', 'fresh_periodic_controls.py',
     'FRESH_PERIODIC_RESULTS.json', None),
    ('fresh_analytic', HERE/'periodic_analytic_crosscheck.py', 'periodic_analytic_crosscheck.py',
     'PERIODIC_ANALYTIC_RESULTS.json', None),
]
with ThreadPoolExecutor(max_workers=4) as ex:
    receipts = list(ex.map(lambda args: replay(*args), jobs))

# Preserve first-party new receipts alongside the scripts, never modify inputs.
for name, output in [('fresh_periodic','FRESH_PERIODIC_RESULTS.json'),
                     ('fresh_analytic','PERIODIC_ANALYTIC_RESULTS.json')]:
    assert not (HERE/output).exists()
    shutil.copy2(TMP/'diagnostic_replays'/name/output, HERE/output)

assert current == current_inventory()
for record in frozen:
    assert sha((SNAPSHOT/record['path']).read_bytes()) == record['sha256']
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS',
          'exact_original_head': HEAD, 'original_frozen_files': frozen, 'current_candidate': current,
          'interpreter': '/usr/bin/python3',
          'python': subprocess.run(['/usr/bin/python3','--version'],capture_output=True,text=True).stdout.strip(),
          'replays': receipts, 'frozen_inputs_unchanged_after_runs': True,
          'scientific_original_and_family_receipts_byte_identical': True,
          'no_git_pr_queue_or_publication_action': True}
(HERE/'REPRODUCTION_AND_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status': result['status'],'original_frozen_files':len(frozen),
                  'current_bound_files':len(current['files']),'replays':receipts},indent=2))
