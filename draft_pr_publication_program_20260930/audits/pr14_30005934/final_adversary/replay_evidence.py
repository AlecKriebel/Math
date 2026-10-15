"""Replay immutable historical/family programs only in this audit's scratch.

Use existing .venv/bin/python; no installation or input mutation is performed.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SCRATCH = HERE / 'tmp' / 'replay'
SCRATCH.mkdir(parents=True, exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


suites = [
    ('author', 'source_snapshot/check_identities.py', 'source_snapshot/check_results.json', 'check_results.json', 8),
    ('historical_independent', 'source_snapshot/independent_review/independent_checks.py', 'source_snapshot/independent_review/independent_results.json', 'independent_results.json', 19),
    ('reproduction_fresh', 'reproduction_family/independent_probes.py', 'reproduction_family/probe_results.json', 'probe_results.json', 29),
    ('stochastic_fresh', 'stochastic_family/exact_checks.py', 'stochastic_family/exact_check_results.json', None, 11),
    ('determinant_jets', 'stochastic_family/conditional_positivity_adversary/determinant_check/check_jets.py', 'stochastic_family/determinant_check_results.txt', None, 144),
]
import sympy
out = {'generated_at_utc':datetime.now(timezone.utc).isoformat(), 'python':sys.version,
       'sympy':sympy.__version__, 'runtime_changed':False, 'runs':[],
       'scope':'Exact computational replay, not certification of analytic limits or external mathematical sources.'}
for label, script_name, receipt_name, generated_name, count in suites:
    directory = SCRATCH/label
    directory.mkdir(exist_ok=True)
    data = (BASE/script_name).read_bytes()
    script = directory/Path(script_name).name
    script.write_bytes(data)
    result = subprocess.run([sys.executable, str(script)],cwd=directory,capture_output=True,check=False)
    (directory/'stdout.txt').write_bytes(result.stdout)
    (directory/'stderr.txt').write_bytes(result.stderr)
    actual = (directory/generated_name).read_bytes() if generated_name else result.stdout
    expected = (BASE/receipt_name).read_bytes()
    identical = actual == expected
    # Preserve exact receipt bytes in the final audit as inspectable evidence.
    (HERE/(label+'_replayed_receipt'+Path(receipt_name).suffix)).write_bytes(actual)
    row = {'suite':label,'script':script_name,'script_sha256':sha(data),
           'returncode':result.returncode,'expected_sha256':sha(expected),
           'actual_sha256':sha(actual),'byte_identical':identical,'recorded_check_count':count,
           'stderr':result.stderr.decode('utf-8',errors='replace')}
    if not identical and receipt_name.endswith('.json'):
        row['json_semantically_identical'] = json.loads(actual) == json.loads(expected)
        if label == 'reproduction_fresh':
            old, new = json.loads(expected), json.loads(actual)
            row['differing_top_level_fields'] = [k for k in old.keys()|new.keys() if old.get(k) != new.get(k)]
            row['stored_timestamp'] = old.pop('generated_at_utc')
            row['replayed_timestamp'] = new.pop('generated_at_utc')
            row['identical_except_generated_timestamp'] = old == new
            row['comparison_note'] = 'The program intentionally emits the current UTC time; only this field is excluded.'
    out['runs'].append(row)
    assert result.returncode == 0, row
    assert identical or row.get('json_semantically_identical') or row.get('identical_except_generated_timestamp'), row
out['passed'] = True
out['total_recorded_checks'] = sum(s[-1] for s in suites)
(HERE/'replay_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'suites':len(suites),'total_recorded_checks':out['total_recorded_checks']},indent=2))
