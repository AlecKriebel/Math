#!/usr/bin/env python3
"""Explicit-exception derivatives of archived originals; do not replace original evidence."""
import ast,hashlib,json,os,shutil,subprocess,sys,threading
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent.parent/'original_submitted_head'
RUNTIME=HERE.parent.parent.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap():return {str(p.relative_to(ORIGINAL)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(ORIGINAL.rglob('*')) if p.is_file()}
BEFORE=snap();receipt=[];lock=threading.Lock()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(RUNTIME))
class Repair(ast.NodeTransformer):
 def __init__(self):self.sites=[]
 def visit_Assert(self,node):
  self.sites.append({'line':node.lineno,'test':ast.unparse(node.test),'message':ast.unparse(node.msg) if node.msg else None})
  fail=ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg] if node.msg else [],keywords=[]),cause=None)
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[fail],orelse=[]),node)
provenance={'UTC_prepared':utc(),'original_archive_before':BEFORE,'method':'Python AST Assert -> If(Not(original_test)): Raise(AssertionError(original_message)); preserve surrounding statements and counter updates. ast.unparse reformats source; no correctness predicate is changed in valid variants.','derivatives':[],'proof_copy':'Unchanged historical original PROOF.md is copied solely to satisfy original verify.py proof_sha256 binding; it is not a current manuscript and is not analytically cleared by these controls.'}
for variant in ['valid','false_identity']:
 d=HERE/variant;(d/'independent_review').mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ORIGINAL/'PROOF.md',d/'PROOF.md')
 for f in ['verify.py','independent_review/independent_check.py']:
  s=(ORIGINAL/f).read_text();mut=None
  if variant=='false_identity':
   old,new=("reduce_poly((D*s*snplus+c*cnplus-C)*den)==0","reduce_poly((D*s*snplus+c*cnplus-C)*den)==1") if f=='verify.py' else ("assert_close(prod,products[0],f'area product {n}/{t}')","assert_close(prod,products[0]+1,f'area product {n}/{t}')")
   if s.count(old)!=1:raise RuntimeError('Nonunique false-identity source '+f)
   s=s.replace(old,new);mut={'before':old,'after':new}
  tree=ast.parse(s);r=Repair();tree=r.visit(tree);ast.fix_missing_locations(tree)
  if any(isinstance(n,ast.Assert) for n in ast.walk(tree)):raise RuntimeError('Unrepaired assertion '+f)
  text='# Explicit-exception derivative; original provenance in DERIVATION_PROVENANCE.json.\n'+ast.unparse(tree)+'\n'
  (d/f).write_text(text)
  provenance['derivatives'].append({'file':str((d/f).relative_to(HERE)),'original_file':f,'original_sha256':sha(ORIGINAL/f),'derivative_sha256':sha(d/f),'replaced_assert_sites':r.sites,'assert_sites_remaining':0,'false_mathematical_identity_mutation':mut})
provenance['historical_proof_copies']=[{'file':v+'/PROOF.md','sha256':sha(HERE/v/'PROOF.md'),'original_sha256':sha(ORIGINAL/'PROOF.md')} for v in ['valid','false_identity']]
(HERE/'DERIVATION_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
(HERE/'RESEARCH_LOG.md').write_text('# Separate original-control repair supplement\n\n'+utc()+' — 15%: prepared explicit-exception derivatives of all2 author and8 reviewer assertion sites; preserved original copies and sealed original audit. Eight required executions pending.\n')
def group(f):
 for variant in ['valid','false_identity']:
  for opt in [False,True]:
   d=HERE/variant;name=variant+'_'+('author' if f=='verify.py' else 'reviewer')+('_optimized' if opt else '_ordinary')
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(d/f)];start=utc()
   r=subprocess.run(cmd,env=env,cwd=d,capture_output=True,text=True)
   (HERE/(name+'.stdout')).write_text(r.stdout);(HERE/(name+'.stderr')).write_text(r.stderr)
   false=variant=='false_identity';expected=1 if false else 0
   if r.returncode!=expected:raise RuntimeError(name+' unexpected exit '+str(r.returncode)+' '+r.stderr)
   archive=ORIGINAL/('verification.json' if f=='verify.py' else 'independent_review/independent_output.json')
   if not false and r.stdout.encode()!=archive.read_bytes():raise RuntimeError(name+' valid output did not preserve archived JSON')
   item={'name':name,'UTC_start':start,'UTC_end':utc(),'argv':cmd,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(RUNTIME)},'derivative_sha256':sha(d/f),'original_script_sha256':sha(ORIGINAL/f),'exit_code':r.returncode,'stdout_file':name+'.stdout','stdout_sha256':sha(HERE/(name+'.stdout')),'stderr_file':name+'.stderr','stderr_sha256':sha(HERE/(name+'.stderr')),'expected_false_identity_rejected':false,'valid_stdout_byte_identical_to_original_archive':not false,'archive_output_sha256':sha(archive)}
   if not false and f=='verify.py':
    shutil.copyfile(d/'verification.json',HERE/(name+'.verification.json'));item['writable_result_sha256']=sha(HERE/(name+'.verification.json'))
   with lock:
    receipt.append(item);(HERE/'REPAIR_EXECUTION_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
    with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — '+str(15+10*len(receipt))+'%: '+name+' exit'+str(r.returncode)+('; false identity rejected' if false else '; exact archived valid output preserved')+'.\n')
   print(name+' exit='+str(r.returncode),flush=True)
# Programs are independent; each program's write-producing normal/-O executions remain sequential.
with ThreadPoolExecutor(max_workers=2) as pool:
 jobs=[pool.submit(group,f) for f in ['verify.py','independent_review/independent_check.py']]
 for job in jobs:job.result()
AFTER=snap()
if BEFORE!=AFTER:raise RuntimeError('Original archive changed')
(HERE/'ORIGINAL_CUSTODY_POST_REPAIR.json').write_text(json.dumps({'UTC':utc(),'before':BEFORE,'after':AFTER,'original_unchanged':True},indent=2)+'\n')
with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — 100% execution complete: all4 valid runs preserve original archived JSON, all4 actual-false controls reject; original20 files unchanged. Separate repair report/manifest still to be sealed.\n')
print('Eight repair executions passed expected outcomes; original archive unchanged.',flush=True)
