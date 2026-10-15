"""Publish this owned checkpoint on fresh native main; no local Git changes."""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import subprocess

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_descending_audit_20261002'
D = Path(__file__).resolve().parent
OUT = D / 'checkpoint_transport' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT.mkdir(parents=True, exist_ok=False)
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE = 'repos/AlecKriebel/Math/'
seq = 0

def api(method, path, payload=None):
    global seq
    seq += 1
    args = [GH, 'api', '--method', method, BASE + path]
    if payload is not None:
        request = OUT / f'{seq:02d}-request.json'
        request.write_text(json.dumps(payload))
        args += ['--input', str(request)]
    run = subprocess.run(args, capture_output=True, timeout=90)
    (OUT / f'{seq:02d}-stdout.json').write_bytes(run.stdout)
    (OUT / f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:
        raise RuntimeError(f'Native call {seq} failed; reconcile retained receipts before mutation retry')
    return json.loads(run.stdout)

intake = json.loads((D / 'INTAKE.json').read_text())
pr = api('GET', 'pulls/246')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == intake['head']
queue = api('GET', 'contents/' + intake['Queue_path'] + '?ref=' + intake['head'])
rows = [r for r in base64.b64decode(queue['content']).decode().splitlines() if '9700040 / AMR-096-0040' in r]
assert len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
assert json.loads((D / 'ROOT_FRESH_FAMILY_VALIDATION.json').read_text())['status'] == 'PASS'

paths = [P / 'RESEARCH_LOG.md', P / 'CURRENT_GOAL_SELECTION_20261013.json']
paths += [f for f in D.iterdir() if f.is_file() and f.suffix in ('.md', '.json', '.py') and f.name != 'PRIORITY_PROGRESS_PUBLICATION_RECEIPT.json']
paths += [f for f in (D / 'submitted').rglob('*') if f.is_file() and '__pycache__' not in f.parts]
paths += [f for f in (D / 'root_reproduction').rglob('*') if f.is_file() and '__pycache__' not in f.parts]
paths += list((D / 'root_history').glob('*.md'))
paths += [D / 'root_source_reading/PRIMARY_RETRIEVAL.json']
for family in ('poisson_dynamics_adversary_01', 'rsk_joint_law_adversary_01', 'source_certificate_adversary_01'):
    folder = D / family
    manifest = folder / 'FINAL_AUDIT_MANIFEST.json'
    data = json.loads(manifest.read_text())
    paths.append(manifest)
    for pin in data.get('public_authored_artifacts', data.get('authored_and_reproduction_artifact_files')):
        path = folder / pin['path']
        assert path.resolve().is_relative_to(folder.resolve())
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
        paths.append(path)
paths += [P / 'next_selection_after_pr248_20261014/SELECTION.json', P / 'next_selection_after_pr248_20261014/PR247_ELIGIBILITY.json']
paths += [f for f in (D / 'root_priority').iterdir() if f.is_file() and f.suffix in ('.md', '.json', '.py')]
paths += [f for f in (D / 'root_priority_reproduction').rglob('*') if f.is_file() and '__pycache__' not in f.parts]
for family, manifestname in [('priority_novelty_falsifier_01','PUBLIC_MANIFEST.json'), ('priority_recent_adversary_01','AUTHORED_FILE_MANIFEST.json')]:
    folder = D / family
    mf = folder / manifestname
    obj = json.loads(mf.read_text())
    paths.append(mf)
    for pin in obj['files']:
        f = folder / pin['path']
        assert f.resolve().is_relative_to(folder.resolve())
        b = f.read_bytes()
        assert len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256']
        paths.append(f)
entries = []
pins = []
for path in sorted(set(paths)):
    assert path.resolve().is_relative_to(P.resolve()) and not path.is_symlink()
    raw = path.read_bytes()
    rel = path.relative_to(ROOT).as_posix()
    entries.append({'path': rel, 'mode': '100644', 'type': 'blob', 'content': raw.decode()})
    pins.append({'path': rel, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})

for attempt in range(4):
    parent = api('GET', 'git/ref/heads/main')['object']['sha']
    tree = api('GET', 'git/commits/' + parent)['tree']['sha']
    new_tree = api('POST', 'git/trees', {'base_tree': tree, 'tree': entries})['sha']
    commit = api('POST', 'git/commits', {'message': 'Checkpoint PR246 explicit earlier covering formulas and independent novelty challenge; final priority review pending', 'tree': new_tree, 'parents': [parent]})['sha']
    try:
        assert api('PATCH', 'git/refs/heads/main', {'sha': commit, 'force': False})['object']['sha'] == commit
        break
    except RuntimeError:
        rejection = json.loads((OUT / f'{seq:02d}-stdout.json').read_text())
        latest = api('GET', 'git/ref/heads/main')['object']['sha']
        if str(rejection.get('status')) != '422' or latest == parent or attempt == 3:
            raise
current = api('GET', 'git/ref/heads/main')['object']['sha']
if current != commit:
    assert api('GET', 'compare/' + commit + '...' + current)['status'] == 'ahead'
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'commit': commit, 'parent': parent,
           'readback_main': current, 'owned_files': pins, 'case_completion_percent': 45,
           'original_PR_head_unchanged': intake['head'], 'native_QUEUE_mutation': False,
           'PR_merge': False, 'Zenodo_publication': False, 'tracker_write': False,
           'shared_checkout_and_index_mutations': 0, 'third_party_reading_copies_excluded': True,
           'transport_receipts': str(OUT)}
(D / 'PRIORITY_PROGRESS_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'owned_files'}, indent=2))
