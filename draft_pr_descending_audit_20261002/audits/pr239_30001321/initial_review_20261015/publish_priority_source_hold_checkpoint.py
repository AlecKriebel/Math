"""Publish this final priority-source hold checkpoint on fresh native main; no local Git changes."""
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
pr = api('GET', 'pulls/239')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == intake['head']
queue = api('GET', 'contents/' + intake['Queue_path'] + '?ref=' + intake['head'])
rows = [r for r in base64.b64decode(queue['content']).decode().splitlines() if '30001321 / OWR-4081-005' in r]
assert len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
assert json.loads((D / 'ROOT_FRESH_FAMILY_VALIDATION.json').read_text())['status'] == 'PASS'

paths = [P / 'RESEARCH_LOG.md', P / 'CURRENT_GOAL_SELECTION_20261013.json']
paths += [f for f in D.iterdir() if f.is_file() and f.suffix in ('.md', '.json', '.py') and f.name != 'PRIORITY_SOURCE_HOLD_PUBLICATION_RECEIPT.json']
paths += [f for f in (D / 'submitted').rglob('*') if f.is_file() and '__pycache__' not in f.parts]
paths += [D / 'root_reproduction/reproduce.py', D / 'root_reproduction/runtime.txt']
for label in ('turn1', 'turn2', 'turn3', 'inherited_independent'):
    paths += [f for f in (D / 'root_reproduction' / label).iterdir() if f.is_file()]
paths += [f for f in (D / 'root_new_control_replays').iterdir() if f.is_file()]
paths += [D / 'root_source_reading/PRIMARY_RETRIEVAL.json']
for family, manifest_name in [('replica_martingale_adversary_01','AUTHORED_MANIFEST.json'), ('final_segment_adversary_01','AUTHORED_MANIFEST.json'), ('source_scope_provenance_adversary_01','PUBLIC_AUTHORED_MANIFEST.json')]:
    folder = D / family
    manifest = folder / manifest_name
    data = json.loads(manifest.read_text())
    pins = data['files']
    if isinstance(pins,dict): pins = [dict(path=k,**v) for k,v in pins.items()]
    paths.append(manifest)
    for pin in pins:
        path = folder / pin['path']
        assert path.resolve().is_relative_to(folder.resolve())
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
        paths.append(path)
selection_folder = P / 'next_selection_after_pr246_20261015'
paths += [selection_folder / 'SELECTION.json', selection_folder / 'INVENTORY_RECEIPT.json', selection_folder / 'gate_next_batch.py', selection_folder / 'intake_pr239.py']
paths += list(selection_folder.glob('PR*_ELIGIBILITY.json'))
# PR246's final scope-skip receipt is prior-disposition bookkeeping, with no new
# scientific evaluation or mutation of that now-ineligible PR.
paths += [P / 'audits/pr246_9700040/initial_review_20261014/PRIORITY_DISPOSITION_PUBLICATION_RECEIPT.json']
paths += [f for f in (D / 'root_priority').iterdir() if f.is_file() and f.suffix in ('.md', '.json', '.py')]
validation = json.loads((D / 'ROOT_FINAL_PRIORITY_VALIDATION.json').read_text())
assert validation['status'] == 'PASS' and len(validation['current_public_seals']) == 7
assert validation['public_pins_verified'] == sum(row['entries'] for row in validation['current_public_seals'])
for sealed in validation['current_public_seals']:
    assert hashlib.sha256((D / sealed['manifest']).read_bytes()).hexdigest() == sealed['sha256']
for family, manifest_name, key in [('priority_historical_01','AUTHORED_MANIFEST.json','files'), ('priority_local_limit_01','PUBLIC_AUTHORED_MANIFEST.json','files'), ('priority_recent_01','AUTHORED_MANIFEST.json','files'), ('priority_bridge_01','PUBLIC_AUTHORED_MANIFEST.json','files'), ('priority_conlon_song_01','PUBLIC_AUTHORED_MANIFEST.json','files'), ('priority_synthesis_adversary_01','PUBLIC_AUTHORED_MANIFEST.json','files'), ('priority_bmp_archival_01','authored_manifest.json','artifacts')]:
    folder = D / family
    manifest = folder / manifest_name
    data = json.loads(manifest.read_text())
    paths.append(manifest)
    for pin in data[key]:
        path = folder / pin['path']
        assert path.resolve().is_relative_to(folder.resolve()) and not set(path.relative_to(folder).parts).intersection({'private_reading','private','private_sources'})
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
        paths.append(path)
paths += [f for f in (D / 'root_priority_reproduction').rglob('*') if f.is_file() and '__pycache__' not in f.parts and not any(part.startswith('synthesis_replay_workspace') for part in f.parts)]
entries = []
pins = []
for path in sorted(set(paths)):
    assert path.resolve().is_relative_to(P.resolve()) and not path.is_symlink()
    raw = path.read_bytes()
    markers = [b'ss'+b'a=', b'ss'+b'b=', b'ss'+b'x=', b'X-Amz-'+b'Signature=', b'access_'+b'token=', b'Authorization: '+b'Bearer ']
    assert not any(marker in raw for marker in markers), str(path)
    rel = path.relative_to(ROOT).as_posix()
    entries.append({'path': rel, 'mode': '100644', 'type': 'blob', 'content': raw.decode()})
    pins.append({'path': rel, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})

for attempt in range(4):
    parent = api('GET', 'git/ref/heads/main')['object']['sha']
    tree = api('GET', 'git/commits/' + parent)['tree']['sha']
    new_tree = api('POST', 'git/trees', {'base_tree': tree, 'tree': entries})['sha']
    commit = api('POST', 'git/commits', {'message': 'Checkpoint PR239 completed adversarial priority synthesis and material original-source hold', 'tree': new_tree, 'parents': [parent]})['sha']
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
           'readback_main': current, 'owned_files': pins, 'case_completion_percent': 60,
           'original_PR_head_unchanged': intake['head'], 'native_QUEUE_mutation': False,
           'PR_merge': False, 'Zenodo_publication': False, 'tracker_write': False,
           'shared_checkout_and_index_mutations': 0, 'third_party_reading_copies_excluded': True,
           'transport_receipts': str(OUT)}
(D / 'PRIORITY_SOURCE_HOLD_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'owned_files'}, indent=2))
