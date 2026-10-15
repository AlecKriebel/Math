#!/usr/bin/env python3
"""Replay immutable historical PR462 code in private temporary copies.

Records optimized-mode failures honestly; no frozen input is modified.
"""
import ast, datetime, hashlib, json, os
from pathlib import Path
import shutil, subprocess, sys, tempfile
P=Path(__file__).resolve().parent
S=P/'source_snapshot/unsolved_math_prioritization/attempts/30005528'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=json.loads((P/'SOURCE_RECEIPT.json').read_text())
 for x in source['files']:
  q=P/'source_snapshot'/x['path']
  if q.stat().st_size!=x['bytes'] or digest(q)!=x['sha256']:raise RuntimeError('Frozen source drift')
 refs=[]
 frozen=json.loads((S/'audit/FROZEN_INPUTS.json').read_text())
 for x in frozen['files']:
  q=S/'release'/x['path']
  if q.stat().st_size!=x['bytes'] or digest(q)!=x['sha256']:raise RuntimeError('Author manifest mismatch')
  refs.append({'kind':'frozen_author','path':'release/'+x['path'],'sha256':x['sha256']})
 manifest=json.loads((S/'audit/AUDIT_MANIFEST.json').read_text())
 for rel,want in manifest['portable_files'].items():
  if digest(S/'audit'/rel)!=want:raise RuntimeError('Audit manifest mismatch')
  refs.append({'kind':'portable_audit','path':'audit/'+rel,'sha256':want})
 runs=[]
 for optimized in (False,True):
  with tempfile.TemporaryDirectory(prefix='pr462-root-replay-') as tmp:
   t=Path(tmp);copy=t/'copy';shutil.copytree(S,copy)
   env=dict(os.environ)
   if optimized:env['PYTHONOPTIMIZE']='1'
   else:env.pop('PYTHONOPTIMIZE',None)
   for name,relative,args,expected in [('author','release/checks/verify_rotation_family.py',[],S/'release/checks/verification_results.json'),('audit','audit/audit_controls.py',['--release',str(copy/'release')],S/'audit/audit_controls.json')]:
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(copy/relative)]+args
    r=subprocess.run(cmd,cwd=t,env=env,capture_output=True)
    out=r.stdout;err=r.stderr.decode().replace(str(t),'<PRIVATE_TEMP>').replace(str(P),'<AUDIT_ROOT>')
    v={'program':name,'optimized':optimized,'optimization_propagated_to_children':optimized,'exit_code':r.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stdout_matches_frozen':out==expected.read_bytes(),'stderr':err,'guards_may_be_elided':name=='author' and optimized}
    if name=='author':v['regenerated_json_matches_frozen']=(copy/'release/checks/verification_results.json').read_bytes()==expected.read_bytes()
    if r.returncode==0:v['result']=json.loads(out)
    runs.append(v)
 for x in source['files']:
  if digest(P/'source_snapshot'/x['path'])!=x['sha256']:raise RuntimeError('Post-replay source drift')
 result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':462,'problem_id':'30005528','head':source['head_sha'],'source_objects_unchanged':len(source['files']),'manifest_references_verified':refs,'interpreter':sys.version,'author_static_assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((S/'release/checks/verify_rotation_family.py').read_text()))),'runs':runs,'all_modes_pass':all(x['exit_code']==0 for x in runs),'limitations':'Author uses assert: optimized author output equality does not attest execution of assertions. Historical audit negative controls must remain active under optimization; any actual failure is retained. Universal proof/source/priority reviewed separately.'}
 (P/'ROOT_REPRODUCTION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'source_objects_unchanged':result['source_objects_unchanged'],'manifest_references_verified':len(refs),'author_static_assert_nodes':result['author_static_assert_nodes'],'runs':[ {k:x[k] for k in ['program','optimized','exit_code','stdout_matches_frozen']} for x in runs]},indent=2))
if __name__=='__main__':main()
