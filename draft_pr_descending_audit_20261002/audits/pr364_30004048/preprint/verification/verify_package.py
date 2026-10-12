#!/usr/bin/env python3
"""Portable exact reproduction; no Git, network, external libraries or file writes."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((R/'MANIFEST.json').read_bytes());files=m['files']
actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
assert actual==set(files)|{'MANIFEST.json'}
assert not any(p.is_symlink() for p in R.rglob('*'))
for n,e in files.items():
 p=R/n;assert stat.S_ISREG(p.lstat().st_mode);b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],n
reference=R/'reference';assert sum(p.is_file() for p in reference.rglob('*'))==41
nested=0
for name in ['SOURCE_GATE_MANIFEST.json','TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json','FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json']:
 p=reference/name
 entries=json.loads(p.read_bytes())['files']
 for e in entries:
  b=(p.parent/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 nested+=len(entries)
assert nested==135
programs=[('reference/verify_turn1.py','reference/TURN_1_CHECKS.json',29175),('reference/verify_turn2.py','reference/TURN_2_CHECKS.json',12749),('reference/verify_turn3.py','reference/TURN_3_CHECKS.json',1831),('reference/review/check_independent.py','reference/review/INDEPENDENT_CHECKS.json',2552),('controls/graph_boundary_controls.py','controls/graph_boundary_expected.json',122568),('controls/polytope_controls.py','controls/polytope_expected.json',357)]
results=[]
for program,expected,count in programs:
 p=R/program;z=subprocess.run([sys.executable,'-B',str(p)],cwd=reference if program.startswith('reference/') else p.parent,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 assert z.returncode==0 and z.stderr==b'',(program,z.returncode,z.stderr)
 assert z.stdout==(R/expected).read_bytes(),program
 obj=json.loads(z.stdout)
 assert obj.get('assertions',obj.get('exact_assertions'))==count,program
 assert obj['status']=='PASS',program
 results.append({'program':program,'whole_stdout_bytes':len(z.stdout),'whole_stdout_sha256':sha(z.stdout),'exact_checks':count,'exit_code':0,'stderr_bytes':0})
assert {p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}==actual
for n,e in files.items():assert sha((R/n).read_bytes())==e['sha256'],n
print(json.dumps({'status':'PASS','original_files':41,'nested_manifest_instances':135,'whole_program_replays':results,'writes':0,'scope':'Exact finite controls, original proof-record custody and whole receipt reproduction. The universal proof is in the manuscript. The exact invariant minima, values, ordering and global priority are not certified by these computations. Raw primary sources and API evidence are omitted; source identities and retrieval recipes are supplied.'},sort_keys=True,indent=2))
