"""Publish only this audit's selected files, without touching the checkout."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_descending_audit_20261002'
D = Path(__file__).resolve().parent
OUT = D / 'checkpoint_transport' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT.mkdir(parents=True, exist_ok=False)
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
seq = 0

def api(method, endpoint, payload=None):
    global seq
    seq += 1
    args = [GH, 'api', '--method', method, endpoint]
    if payload is not None:
        request = OUT / f'{seq:02d}-request.json'
        request.write_text(json.dumps(payload))
        args += ['--input', str(request)]
    r = subprocess.run(args, capture_output=True)
    (OUT / f'{seq:02d}-stdout.json').write_bytes(r.stdout)
    (OUT / f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    if r.returncode:
        raise RuntimeError(f'Native API call {seq} failed; receipts retained')
    return json.loads(r.stdout)

pr = api('GET', 'repos/AlecKriebel/Math/pulls/254')
intake = json.loads((D / 'INTAKE.json').read_text())
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == intake['head']
q = api('GET', 'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref=' + intake['head'])
row = next(x for x in base64.b64decode(q['content']).decode().splitlines() if '5100020 / AMR-050-0020' in x)
assert row.split('|')[8].strip() == 'claimed_solved'
paths = [P / 'RESEARCH_LOG.md', P / 'CURRENT_GOAL_SELECTION_20261013.json',
         D / 'INTAKE.json', D / 'RESEARCH_LOG.md', D / 'ROOT_INTAKE_AND_REPRODUCTION.md',
         D / 'publish_owned_checkpoint.py', D / 'root_reproduce.py', D / 'root_replay_fresh.py', D / 'PRIMARY_SOURCE_HASH_CHECKS.json', P / 'audits/pr255_5100022/initial_review_20261013/PRIORITY_DISPOSITION_PUBLICATION_RECEIPT.json']
paths += sorted((D / 'submitted/unsolved_math_prioritization/attempts/5100020').rglob('*'))
paths += sorted((D / 'root_reproduction').glob('*.json'))
paths += [p for p in [D / 'ROOT_PROOF_ANALYSIS.md', D / 'ROOT_MATHEMATICAL_ACCEPTANCE.md'] if p.exists()]
for folder in ['meromorphic_adversary_01', 'geometric_adversary_01']:
    paths += sorted((D / folder).glob('*'))
paths += sorted((D / 'root_fresh_reproduction').rglob('*.json'))
paths = [p for p in paths if p.is_file()]
progress = json.loads((P / 'CURRENT_GOAL_SELECTION_20261013.json').read_text())
entries = [{'path': p.relative_to(ROOT).as_posix(), 'mode': '100644',
            'type': 'blob', 'content': p.read_text()} for p in paths]
for attempt in range(4):
    parent = api('GET', 'repos/AlecKriebel/Math/git/ref/heads/main')['object']['sha']
    tree = api('GET', 'repos/AlecKriebel/Math/git/commits/' + parent)['tree']['sha']
    newtree = api('POST', 'repos/AlecKriebel/Math/git/trees', {'base_tree': tree, 'tree': entries})['sha']
    commit = api('POST', 'repos/AlecKriebel/Math/git/commits',
                 {'message': 'Checkpoint k403a mathematical audit evidence; ' + progress['current_stage'],
                  'tree': newtree, 'parents': [parent]})['sha']
    try:
        assert api('PATCH', 'repos/AlecKriebel/Math/git/refs/heads/main',
                   {'sha': commit, 'force': False})['object']['sha'] == commit
        break
    except RuntimeError:
        rejection = json.loads((OUT / f'{seq:02d}-stdout.json').read_text())
        latest = api('GET', 'repos/AlecKriebel/Math/git/ref/heads/main')['object']['sha']
        if rejection.get('status') != '422' or latest == parent or attempt == 3:
            raise
current = api('GET', 'repos/AlecKriebel/Math/git/ref/heads/main')['object']['sha']
if current != commit:
    assert api('GET', 'repos/AlecKriebel/Math/compare/' + commit + '...' + current)['status'] == 'ahead'
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'commit': commit,
           'parent': parent, 'readback_main': current, 'case_completion_percent': progress['case_completion_percent'],
           'owned_files': len(entries), 'shared_checkout_index_mutations': 0,
           'copyright_source_reading_copies_excluded': True, 'transport_receipts': str(OUT),
           'file_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(D / ('CHECKPOINT_' + str(progress['case_completion_percent']) + '_RECEIPT.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'file_hashes'}, indent=2))
