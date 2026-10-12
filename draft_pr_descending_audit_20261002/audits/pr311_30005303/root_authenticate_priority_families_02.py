"""Authenticate closed audit artifacts and replay exact falsification controls.

This checks bytes and execution evidence; it does not assert full PDF reading or novelty.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, sys
A = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
load = lambda p: json.loads(p.read_bytes())
assert sys.flags.optimize == 0
D = A/'root_priority_replay_private_02'; D.mkdir(exist_ok=False)
def measured(p):
 b = p.read_bytes()
 return dict(bytes=len(b), sha256=sha(b), mode=oct(stat.S_IMODE(p.stat().st_mode)))
F=A/'priority_factorization'; C=A/'priority_closure'
expected={
 F/'FINAL_PRIORITY_REPORT.md':'0f328de205ba243eb2ada09a07f0bf4488e9a40e8dc36b7643c5716e25da8dff',
 F/'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json':'f4719a1af2d90c98bc14db57d475809aeae72721a8dad8669aa647d8a941d579',
 F/'FINAL_SEAL_RECEIPT.json':'db1d49b148c4e1a2877398ccb5052c4fe9212655b9f702da159118b68e9d13d2',
 C/'FINAL_PRIORITY_REPORT.md':'205e8114aed491f04b54f8f7dda67d09c741d5ac78663f1fc8e936796bb783f2',
 C/'KS_CONTRACTION_SPECIALIZATION.md':'2058344765713485abe762667cb1f8cf7d272c310d16a0e90bbf65250613553e',
 C/'INPUT_OUTPUT_SHA_MANIFEST.json':'4855a0c002716e42a3416c12b58328ac6752ad6caabb9a29a53c97fcaf60d20f',
 C/'FINAL_SEAL.json':'df1bcc94bb549147217a4968a42932b895de7c49238e1504ef07fb75ac81ad3c',
}
for p,h in expected.items():
 m=measured(p); assert m['sha256']==h and m['mode']=='0o444'
fm=load(F/'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json'); cm=load(C/'INPUT_OUTPUT_SHA_MANIFEST.json'); cs=load(C/'FINAL_SEAL.json')
all_pins={}
for row in fm['audit_files']:
 p=F/row['relative_path']; m=measured(p); e=row['final_actual_measurement']
 assert m=={k:e[k] for k in ['bytes','sha256','mode']} and row['bytes_unchanged_by_seal']
 assert row['old_actual_measurement']['sha256']==m['sha256']
 all_pins[p]=m
for row in cs['files']:
 p=C/row['path']; m=measured(p)
 assert m==dict(bytes=row['bytes'],sha256=row['sha256_after'],mode=row['measured_final_mode'])
 assert row['sha256_before']==row['sha256_after'] and row['bytes_unchanged']
 all_pins[p]=m
for row in fm['candidate_input_rechecks']:
 p=Path(row['absolute_path']); m=measured(p); e=row['final_measurement']
 assert m=={k:e[k] for k in ['bytes','sha256','mode']} and row['unchanged_since_read'] and not row['written_by_audit']
for row in cm['candidate_inputs']:
 p=Path(row['path']); m=measured(p)
 assert m['sha256']==row['sha256'] and m['bytes']==row['bytes'] and m['mode']==row['measured_old_mode']
native=[]
for row in load(F/'native_command_index.json')['captures']:
 p=F/row['private_capture']; b=p.read_bytes(); assert sha(b)==row['sha256'] and len(b)==row['bytes']
 j=json.loads(b)
 for k in ['stdout','stderr']:
  assert sha(j[k+'_utf8'].encode())==j[k+'_sha256']==row[k+'_sha256']
 assert j['exit_code']==row['exit_code']
 native.append(dict(path=row['private_capture'],start=j['started_actual_utc'],end=j['ended_actual_utc'],exit_code=j['exit_code']))
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
def run(label,args):
 j=dict(argv=args,cwd=str(A),started_utc=utc(),source=measured(Path(args[1])),optimization_disabled=True)
 (D/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=A,capture_output=True,env=env)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(label+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),stderr_bytes=len(r.stderr),stderr_sha256=sha(r.stderr))
 (D/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 assert r.returncode==0 and not r.stderr
 return j,json.loads(r.stdout)
fj,fout=run('factorization_laws',[sys.executable,str(F/'verify_laws.py'),'--output',str(D/'factorization_laws.json')])
assert (D/'factorization_laws.json').read_bytes()==(F/'comparison_laws_exact_results.json').read_bytes()==(F/'comparison_laws_reproduction.json').read_bytes()
cj,cout=run('closure_boundary',[sys.executable,str(C/'boundary_controls.py')])
assert cout==json.loads(load(C/'BOUNDARY_CONTROLS_CAPTURE.json')['stdout'])
assert all(measured(p)==m for p,m in all_pins.items())
j=dict(actual_utc=utc(),status='PASS_CLOSED_PRIORITY_FAMILIES_BYTES_MODES_AND_SCIENTIFIC_REPLAYS',
 report_body_read_scope='ROOT fully read both final reports, KS specialization, ledgers, factor verification code and closure control code. Selected primary bodies separately recorded; no claim all downloaded sources were fully read.',
 factorization_sealed_files=len(fm['audit_files']),closure_sealed_files=len(cs['files']),candidate_inputs_unchanged=True,
 native_factorization_captures_authenticated=native,native_capture_limit=fm['native_capture_limits'],
 replay=[fj,cj],exact_law_output=measured(D/'factorization_laws.json'),law_summary=fout['law_checks'],boundary_controls=cout,
 immutable_audit_bytes_and_modes_preserved=True,priority_verdict='C2/C3 exact prior witness accepted; C1 bounded priority/publication judgment remains pending fresh reviewer.',math_percent=100,priority_percent=70,workflow_percent=40)
out=A/'ROOT_CLOSED_PRIORITY_FAMILIES_AUTHENTICATION_02.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
