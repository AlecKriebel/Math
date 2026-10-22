"""Fail-closed local-only replay of the complete bounded certificates."""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
NAMES={'REPORT.md','INDEPENDENT_REVIEW.md','checker_regression.json','exact_results.json','exact_search.py','independent_lattice.py','independent_lattice_results.json','independent_ordered.cpp','independent_ordered_results.txt','independent_seven.cpp','independent_seven_results.txt','lattice_check.py','lattice_results.json','seven_point_check.cpp','seven_point_results.txt','PUBLIC_SOURCE_METADATA.json','SOURCE_GATE.md','RESULT.md','check_regressions.py','replay.py','AST_PROVENANCE.json','CODE_PROVENANCE.json','MANIFEST.json'}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def no_sockets(event,args):
    if event.startswith('socket.'):
        raise PermissionError('socket use denied')

sys.addaudithook(no_sockets)
sys.dont_write_bytecode=True
entries=list(os.scandir(BASE))
need({e.name for e in entries}==NAMES, 'inventory mismatch before content read')
need(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries), 'nonregular inventory before content read')
manifest=json.loads((BASE/'MANIFEST.json').read_text())
need(set(manifest['files'])==NAMES-{'MANIFEST.json'}, 'manifest inventory')
for name,record in manifest['files'].items():
    raw=(BASE/name).read_bytes()
    need(len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'], 'payload mismatch: '+name)
asts=json.loads((BASE/'AST_PROVENANCE.json').read_text())
need(set(asts)=={n for n in NAMES if n.endswith('.py')}, 'whole-module AST inventory')
for name,digest in asts.items():
    tree=ast.dump(ast.parse((BASE/name).read_text()),include_attributes=False)
    need(hashlib.sha256(tree.encode()).hexdigest()==digest,'whole-module AST mismatch: '+name)
provenance=json.loads((BASE/'CODE_PROVENANCE.json').read_text())
need(set(provenance['sources'])=={n for n in NAMES if n.endswith(('.py','.cpp'))},'code provenance inventory')
for name,record in provenance['sources'].items():
    need(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==record['sha256'],'source provenance: '+name)
if '--inventory-only' in sys.argv:
    print(json.dumps({'verdict':'PASS','inventory_files':len(NAMES),'whole_module_asts':len(asts),'source_files':len(provenance['sources'])},sort_keys=True))
    sys.exit(0)

CHILD="import sys,runpy; sys.dont_write_bytecode=True; exec(\"def guard(event,args):\\n if event.startswith('socket.'):\\n  raise PermissionError('socket use denied')\"); sys.addaudithook(guard); runpy.run_path(sys.argv[1],run_name='__main__')"
reports={}
def execute(command,cwd):
    done=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=1800,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    need(done.returncode==0,'execution failed: '+str(command)+'\n'+done.stderr)
    need(done.stderr=='','unexpected stderr: '+done.stderr)
    return done.stdout

def strip_times(rows):
    expected_keys={'p','m','witness','unordered_counts','smaller_sizes','candidates_at_witness','seconds'}
    need(type(rows) is list and len(rows)==10, 'exact result requires ten rows')
    for row in rows:
        need(type(row) is dict and set(row)==expected_keys, 'exact result row keys')
        seconds=row['seconds']
        need(type(seconds) in (int,float) and math.isfinite(seconds) and seconds>=0, 'invalid row-level seconds')
    # Exempt only this validated row-level timing field, never nested fields.
    return [{k:v for k,v in row.items() if k!='seconds'} for row in rows]

with tempfile.TemporaryDirectory(prefix='unique_sum_replay_') as temp:
    work=Path(temp)
    for name in NAMES:
        shutil.copyfile(BASE/name,work/name)
    py=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',CHILD]
    stdout=execute(py+[str(work/'exact_search.py')],work)
    expected=json.loads((BASE/'exact_results.json').read_text())
    actual=json.loads((work/'exact_results.json').read_text())
    need(strip_times(actual)==strip_times(expected),'exact search complete result mismatch')
    lines=[ast.literal_eval(line) for line in stdout.splitlines()]
    # Python prints tuples before serializing them as JSON lists.
    need(json.loads(json.dumps(strip_times(lines)))==strip_times(expected),'exact search stdout mismatch')
    reports['exact_search']={'verdict':'PASS','primes':10,'all_fields_except_seconds_equal':True}
    # Restore original input bytes to preserve exact provenance for subsequent checks.
    shutil.copyfile(BASE/'exact_results.json',work/'exact_results.json')
    for script,output in [('lattice_check.py','lattice_results.json'),('independent_lattice.py','independent_lattice_results.json')]:
        stdout=execute(py+[str(work/script)],work)
        need((work/output).read_bytes()==(BASE/output).read_bytes(),script+' output bytes mismatch')
        need(json.loads(stdout)==json.loads((BASE/output).read_text()),script+' stdout mismatch')
        reports[script]={'verdict':'PASS','exact_output_bytes':len((work/output).read_bytes())}
    for source,output in [('seven_point_check.cpp','seven_point_results.txt'),('independent_ordered.cpp','independent_ordered_results.txt'),('independent_seven.cpp','independent_seven_results.txt')]:
        binary=work/(source+'.bin')
        execute(['g++','-std=c++17','-O2',str(work/source),'-o',str(binary)],work)
        stdout=execute([str(binary)],work)
        need(stdout.encode()==(BASE/output).read_bytes(),source+' exact output mismatch')
        reports[source]={'verdict':'PASS','exact_output_bytes':len(stdout.encode()),'sha256':hashlib.sha256(stdout.encode()).hexdigest()}
    regressions=json.loads(execute(py+[str(work/'check_regressions.py')],work))
    need(regressions['verdict']=='PASS','mathematical regressions')
    reports['regressions']=regressions
print(json.dumps({'verdict':'PASS','optimized':sys.flags.optimize,'inventory_files':len(NAMES),'whole_module_asts':len(asts),'socket_audit_guard':True,'reports':reports},indent=2,sort_keys=True))
