#!/usr/bin/env python3
"""Capture actual rejection of substantive formula mutants by the repaired control."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;ROOT=A/'root_preprint_private/dual_replay_v04/extracted/qss-self-duality-verification';OUT=A/'root_preprint_private/formula_mutants_v04'
assert not OUT.exists();OUT.mkdir()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
original=ROOT/'controls/verify_intrinsic.py';body=original.read_text();before={str(p):pin(p) for p in (original,ROOT/'controls/construction.json')}
correct='rank(join(transpose(twist(twist(v2,k.sigma),k.sigma)),transpose(twist(twist(f2,k.tau),k.tau))),k)'
assert body.count(correct)==1
mutants={'bare_rows':'rank(join(transpose(f2),transpose(v2)),k)',
 'squared_directions_swapped':'rank(join(transpose(twist(twist(v2,k.tau),k.tau)),transpose(twist(twist(f2,k.sigma),k.sigma))),k)',
 'single_instead_of_squared_twists':'rank(join(transpose(twist(v2,k.sigma)),transpose(twist(f2,k.tau))),k)'}
receipts=[]
for name,wrong in mutants.items():
 directory=OUT/name;directory.mkdir();script=directory/'verify_intrinsic.py';script.write_text(body.replace(correct,wrong));(directory/'construction.json').write_bytes((ROOT/'controls/construction.json').read_bytes())
 for label,exe in [('system',sys.executable),('bundled','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]:
  tag=name+'_'+label;argv=[exe,'-B',str(script)]
  pre=dict(utc=utc(),argv=argv,cwd=str(directory),controller=pin(Path(__file__)),mutant_code=pin(script),replacement=dict(correct=correct,wrong=wrong),expected_exit_status=1)
  (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
  r=subprocess.run(argv,cwd=directory,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))
  (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
  rec=dict(pre,end_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
  (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
  assert r.returncode==1 and b'check_dense_kernel_formulas' in r.stderr and b'AssertionError' in r.stderr and not r.stdout
  assert pin(script)==pre['mutant_code'] and {p:pin(Path(p)) for p in before}==before
summary=dict(utc=utc(),status='ALL_SUBSTANTIVE_FORMULA_MUTANTS_REJECTED',mutants=list(mutants),actual_negative_run_count=6,two_runtimes=True,current_public_code_and_input_unchanged=True,actual_native_receipts=receipts,publication_clearance=False)
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='actual_native_receipts'},indent=2))
