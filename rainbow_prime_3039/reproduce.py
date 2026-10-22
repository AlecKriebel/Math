"""Replay bounded checks without modifying historical results or retaining binaries."""
import argparse
import json
import platform
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
checks = []

def run(command, filename):
    result = subprocess.run([str(x) for x in command], cwd=ROOT, text=True,
                            capture_output=True, check=True)
    (out / filename).write_text(result.stdout)
    if result.stderr:
        (out / (filename + '.stderr')).write_text(result.stderr)
    return result.stdout

def same_json(actual, expected, label):
    assert json.loads(actual) == json.loads((ROOT / expected).read_text()), label
    checks.append(label)

same_json(run([sys.executable, ROOT/'analytic/verify_counts.py'], 'analytic.json'),
          'analytic/verification_results.json', 'analytic exact outputs match')
same_json(run([sys.executable, ROOT/'audit/independent_checks.py'], 'audit.json'),
          'audit/independent_results.json', 'independent audit exact outputs match')
same_json(run([sys.executable, ROOT/'computation/interval_transfer.py'], 'interval.json'),
          'computation/interval_checks.json', '400 interval tests match')
structural = run([sys.executable, ROOT/'structural/check_propagation.py'], 'structural.txt')
assert structural == (ROOT/'structural/verification.txt').read_text()
checks.append('structural outputs match')
python_runs = run([sys.executable, ROOT/'computation/verify.py', '--brute'], 'python_search.jsonl')
old_python = [json.loads(x) for x in (ROOT/'computation/independent_results.jsonl').read_text().splitlines()]
new_python = [json.loads(x) for x in python_runs.splitlines()]
assert len(old_python) == len(new_python) == 5
for old, new in zip(old_python, new_python):
    assert {k:v for k,v in old.items() if k!='seconds'} == {k:v for k,v in new.items() if k!='seconds'}
checks.append('five independent exhaustive searches match, excluding timings')
run([sys.executable, ROOT/'computation/verify.py', ROOT/'computation/relaxed_results.jsonl'], 'relaxed_validation.txt')
checks.append('all historical relaxed SAT witnesses validated, not balanced claims')
old_cpp = {r['p']:r for r in map(json.loads,(ROOT/'computation/results.jsonl').read_text().splitlines())}
with tempfile.TemporaryDirectory(prefix='rainbow4ap-') as build:
    binary = Path(build)/'search'
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'computation/search.cpp'),'-o',str(binary)],check=True)
    results=[]
    for p in (5,7,11,13,17,19,23,29):
        result=json.loads(subprocess.check_output([str(binary),str(p),'120'],text=True))
        results.append(result)
        assert result['status']=='UNSAT_EXHAUSTIVE', result
        assert all(result[k] == v for k,v in old_cpp[p].items() if k != 'seconds')
        assert result['min_size'] == p//4 and result['max_size'] == (p+3)//4
    (out/'cpp_search.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in results))
    checks.append('eight C++ exhaustive searches match, excluding timings')
    prime31=json.loads(run([binary,'31','20'], 'prime31.json'))
    assert prime31['status'] in ('UNKNOWN_TIMEOUT','UNSAT_EXHAUSTIVE','SAT')
    if prime31['status']=='SAT':
        run([sys.executable,ROOT/'computation/verify.py',out/'prime31.json'],'prime31_validation.txt')
metadata={'python':sys.version,'platform':platform.platform(),
          'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
          'checks':checks,'prime31_status':prime31['status'],
          'timings_and_timeout_nodes_are_machine_dependent':True}
(out/'summary.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
