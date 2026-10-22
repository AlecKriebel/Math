#!/usr/bin/env python3
"""Disposable unchanged and actual-false-identity execution, never importing author code."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,shutil,datetime,ast
HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'original_submitted_head'
RUNTIME=HERE.parent.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {str(p.relative_to(ORIGINAL)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(ORIGINAL.rglob('*')) if p.is_file()}
before=snapshot()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(RUNTIME))
receipts=json.loads((HERE/'original_execution_receipts.json').read_text()).get('receipts',[]) if (HERE/'original_execution_receipts.json').exists() else []
completed_names={r['name'] for r in receipts}
for variant in ['unchanged','false_identity']:
 d=HERE/('disposable_'+variant);(d/'independent_review').mkdir(parents=True,exist_ok=True)
 for f in ['PROOF.md','verify.py','independent_review/independent_check.py']:
  shutil.copyfile(ORIGINAL/f,d/f)
 edits=[]
 if variant=='false_identity':
  edits=[('verify.py',"reduce_poly((D*s*snplus+c*cnplus-C)*den)==0","reduce_poly((D*s*snplus+c*cnplus-C)*den)==1"),('independent_review/independent_check.py',"assert_close(prod,products[0],f'area product {n}/{t}')","assert_close(prod,products[0]+1,f'area product {n}/{t}')")]
  for f,old,new in edits:
   p=d/f;s=p.read_text()
   if s.count(old)!=1:raise RuntimeError('Mutation source not unique: '+f)
   p.write_text(s.replace(old,new))
 for f in ['verify.py','independent_review/independent_check.py']:
  for optimize in [False,True]:
   name=variant+'_'+('author' if f=='verify.py' else 'reviewer')+('_optimized' if optimize else '_ordinary')
   if name in completed_names:continue
   t=datetime.datetime.now(datetime.timezone.utc).isoformat();cmd=[sys.executable]+(['-O'] if optimize else [])+[str(d/f)]
   r=subprocess.run(cmd,cwd=d,env=env,capture_output=True,text=True)
   (HERE/(name+'.stdout')).write_text(r.stdout);(HERE/(name+'.stderr')).write_text(r.stderr)
   data=None
   if r.returncode==0:
    data=json.loads(r.stdout)
   expected=ORIGINAL/('verification.json' if f=='verify.py' else 'independent_review/independent_output.json')
   archived=json.loads(expected.read_text())
   receipt={'name':name,'UTC_start':t,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'script_sha256':sha(d/f),'exit_code':r.returncode,'stdout_file':name+'.stdout','stdout_sha256':sha(HERE/(name+'.stdout')),'stderr_file':name+'.stderr','stderr_sha256':sha(HERE/(name+'.stderr')),'stdout_json':data,'archive_json_semantically_equal':data==archived if data is not None else False,'archive_json_sha256':sha(expected),'mutations':[{'file':q,'before':o,'after':n} for q,o,n in edits if q==f]}
   if f=='verify.py' and (d/'verification.json').exists():
    # Preserve exact writable result output separately from stdout; it can be stale after failure.
    dest=HERE/(name+'.verification.json');shutil.copyfile(d/'verification.json',dest)
    receipt['writable_result_sha256']=sha(dest);receipt['writable_result_may_be_stale']=r.returncode!=0
   receipts.append(receipt)
   (HERE/'original_execution_receipts.json').write_text(json.dumps({'receipts':receipts,'original_before':before},indent=2)+'\n')
   print(name+' exit='+str(r.returncode)+' same_archive='+str(receipt['archive_json_semantically_equal']),flush=True)
after=snapshot()
if before!=after:raise RuntimeError('Original custody changed')
assertion_sites={f:[{'line':n.lineno,'expression':ast.unparse(n.test)} for n in ast.walk(ast.parse((ORIGINAL/f).read_text())) if isinstance(n,ast.Assert)] for f in ['verify.py','independent_review/independent_check.py']}
result={'receipts':receipts,'original_before':before,'original_after':after,'original_unchanged':True,'assertion_sites':assertion_sites,'runtime_reused_readonly':str(RUNTIME),'historical_original_runtime_flags':'unknown','provenance':'Only original scripts and PROOF.md copied into disposable layout. Mutations explicitly recorded. No original module imported or original output written.'}
(HERE/'original_execution_receipts.json').write_text(json.dumps(result,indent=2)+'\n')
