"""Replay the closed first whole adversary without modifying its artifacts."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
H = Path(__file__).resolve().parent
F = H / 'current_whole_adversary'
D = H / 'tmp/root_new1_review/reviewer'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
def closure():
    m = load(F / 'MANIFEST.json')
    assert sha((F / 'MANIFEST.json').read_bytes()) == '94fccf1191d886a8c0eaf4869d1af83324359940e8eae192eced8bdcc343c45f'
    for z in m['files']:
        b = (F / z['path']).read_bytes()
        assert len(b) == z['bytes'] and sha(b) == z['sha256'], z['path']
    return m
m = closure()
D.mkdir(parents=True, exist_ok=True)
for z in m['files']:
    q = D / z['path']; q.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(F / z['path'], q)
shutil.copytree(H / 'reviewed_candidate', D.parent / 'reviewed_candidate', dirs_exist_ok=True)
shutil.copyfile(H / 'ROOT_NI2026_RETRIEVAL.json', D.parent / 'ROOT_NI2026_RETRIEVAL.json')
runs = []
for name in ['reproduce.py', 'independent_controls.py']:
    r = subprocess.run(['/usr/bin/python3', str(D / name)], capture_output=True, timeout=240)
    (D / (name + '.root_stdout')).write_bytes(r.stdout)
    (D / (name + '.root_stderr')).write_bytes(r.stderr)
    assert r.returncode == 0 and not r.stderr, (name, r.returncode, r.stderr.decode())
    runs.append({'program': name, 'implementation_sha256': sha((D / name).read_bytes()), 'exit': r.returncode, 'stderr_empty': True, 'stdout': json.loads(r.stdout)})
old, new = load(F / 'REPRODUCTION_RESULTS.json'), load(D / 'REPRODUCTION_RESULTS.json')
assert {k:v for k,v in old.items() if k != 'utc'} == {k:v for k,v in new.items() if k != 'utc'}
a, b = load(F / 'INDEPENDENT_CONTROLS.json'), load(D / 'INDEPENDENT_CONTROLS.json')
for k in ['checks_passed', 'independent_validator_mutants_rejected', 'actual_current_code_mutants_rejected', 'checks', 'mutants', 'mandatory_administrative_failure', 'mathematical_failure_found', 'scope']:
    assert a[k] == b[k], k
assert [{k:v for k,v in z.items() if k != 'stderr_sha256'} for z in a['actual_mutations']] == [{k:v for k,v in z.items() if k != 'stderr_sha256'} for z in b['actual_mutations']]
for z in m['files']:
    p = F / z['path']
    if p.suffix == '.json': load(p)
    elif p.suffix == '.jsonl':
        for line in p.read_bytes().splitlines(): json.loads(line)
assert closure() == m
receipt = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'closed_members_verified_before_and_after': len(m['files']), 'closed_manifest_sha256': sha((F / 'MANIFEST.json').read_bytes()), 'actual_root_runs': runs, 'nine_outer_replays_equal_except_actual_clock': True, 'independent_controls_equal_except_private_traceback_path_hashes': True, 'actual_mutant_assertions_and_implementation_hashes_equal': True, 'all_closed_json_fully_parsed': True, 'all_closed_artifacts_unchanged': True, 'mathematical_finding': 'PASS universal proof and exact earlier-construction attribution; finite controls are supplemental', 'administrative_finding': 'One mandatory inherited current-looking budget/model/compute/literature timestamp correction remains; no clean gate transferred', 'attempts_added': 0, 'workflow_completion_estimate_percent': 75}
(H / 'ROOT_NEW1_ACTUAL_REPRODUCTION.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
