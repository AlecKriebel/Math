#!/usr/bin/env python3
"""One-shot actual capture of independent formula falsification."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;OUT=A/'root_preprint_private/formula_falsification_001'
assert not OUT.exists();OUT.mkdir()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
code=A/'root_intrinsic_formula_diagnostic.py';original=A/'intrinsic_invariants/public/verify_intrinsic.py'
inputs={str(p):pin(p) for p in (code,original)}
assert inputs[str(original)]['sha256']=='fbbc16f32a989f723ff9271ef771019919227c1fe81dc3931c49a9c9e460f954'
receipts=[];outputs={}
for label,exe in [('system',sys.executable),('bundled','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]:
 for mode,args in [('independent',[]),('with_original',[str(original)])]:
  tag=label+'_'+mode;argv=[exe,'-B',str(code),*args]
  pre=dict(utc=utc(),argv=argv,cwd=str(A),inputs=inputs,controller=pin(Path(__file__)),interpreter=pin(Path(exe).resolve()),environment_overrides={'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
  (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
  r=subprocess.run(argv,cwd=A,capture_output=True,env=dict(os.environ,**pre['environment_overrides']))
  (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
  rec=dict(pre,end_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
  (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
  assert r.returncode==0 and not r.stderr
  assert {p:pin(Path(p)) for p in inputs}==inputs
  v=json.loads(r.stdout);assert v['repair_required'] and len(v['witnesses'])==2
  assert all(w['delta']==0 and w['dual_delta']==w['corrected']==w['semantic_kernel_codimension']==1 and w['bare']==0 for w in v['witnesses'])
  outputs[(label,mode)]=r.stdout
assert all(outputs[('system',m)]==outputs[('bundled',m)] for m in ('independent','with_original'))
summary=dict(utc=utc(),status='ROOT_INDEPENDENT_EXACT_COUNTEREXAMPLE_REPRODUCED',main_theorem_valid=True,supplementary_generic_helper_repair_required=True,actual_native_receipts=receipts,original_control_unchanged=True,two_runtime_output_bytes_equal=True,publication_clearance=False)
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='actual_native_receipts'},indent=2))
