#!/usr/bin/env python3
"""Normal, optimized, relocated and negative publication integrity controls."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).absolute().parent
PIN=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
def need(v,m):
 if not v:raise RuntimeError(m)
def run(root,opt=False,pin=PIN):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
 return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(root/'verify_package.py'),'--expected-manifest',pin],cwd='/',env=env,capture_output=True,text=True,timeout=300)
def rawedit(r,n):
 p=r/n;p.write_bytes(p.read_bytes()+b' ')
def resign(r):
 p=r/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text())
 for x in m['files']:
  b=(r/x['path']).read_bytes();x.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 p.write_text(json.dumps(m,sort_keys=True)+'\n')
def scope(r):
 p=r/'VERDICT.json';j=json.loads(p.read_text());j['existential_attainment_disproved']=True;p.write_text(json.dumps(j));resign(r)
def alias(r):
 p=r/'author/PROOF.md';b=p.read_bytes();p.unlink();o=r.parent/'outside-proof';o.write_bytes(b);p.symlink_to(o)
def dupe(r):
 p=r/'PUBLICATION_MANIFEST.json';p.write_bytes(b'{"problem_id":6200061,'+p.read_bytes()[1:])
def pathmut(r):
 p=r/'PUBLICATION_MANIFEST.json';j=json.loads(p.read_text());j['files'][0]['path']='../unsafe';p.write_text(json.dumps(j))
def resauthor(r):
 rawedit(r,'author/PROOF.md');resign(r)
def main():
 controls=[];clean=[]
 for opt in [False,True]:
  p=run(ROOT,opt);need(p.returncode==0,p.stderr);j=json.loads(p.stdout);j.pop('optimized');clean.append(j);controls.append({'case':'original','optimized':opt,'passed':True})
 with tempfile.TemporaryDirectory(prefix='problem61_publication_') as td:
  tmp=Path(td);rel=tmp/'relocated';shutil.copytree(ROOT,rel)
  for opt in [False,True]:
   p=run(rel,opt);need(p.returncode==0,p.stderr);j=json.loads(p.stdout);j.pop('optimized');clean.append(j);controls.append({'case':'relocated','optimized':opt,'passed':True})
  cases=[('changed_proof',lambda r:rawedit(r,'author/PROOF.md')),('changed_audit',lambda r:rawedit(r,'audit/AUDIT_REPORT.md')),('same_size_result',lambda r:(r/'author/RESULTS.json').write_bytes((r/'author/RESULTS.json').read_bytes().replace(b'80',b'81',1))),('missing_file',lambda r:(r/'author/RESULTS.json').unlink()),('extra_file',lambda r:(r/'source.pdf').write_bytes(b'%PDF forbidden')),('extra_directory',lambda r:(r/'unlisted').mkdir()),('nested_manifest',lambda r:((r/'unlisted').mkdir(),(r/'unlisted/MANIFEST.json').write_text('{}'))),('damaged_zip',lambda r:rawedit(r,'archives/KLEINIAN_BOUNDARY_6200061_AUTHOR_SAFE_FREEZE.zip')),('changed_manifest',lambda r:rawedit(r,'PUBLICATION_MANIFEST.json')),('unsafe_manifest_path',pathmut),('duplicate_json_key',dupe),('symlink_member',alias),('rehash_claim_inflation',scope),('rehash_proof_change',resauthor)]
  for name,fn in cases:
   r=tmp/name;shutil.copytree(ROOT,r);fn(r)
   for opt in [False,True]:
    p=run(r,opt);need(p.returncode!=0,'mutation accepted '+name);controls.append({'case':name,'optimized':opt,'rejected':True})
  link=tmp/'linked';link.symlink_to(rel,target_is_directory=True)
  for opt in [False,True]:
   for name,r,pin in [('ancestor_symlink',link,PIN),('wrong_external_pin',rel,'0'*64)]:
    p=run(r,opt,pin);need(p.returncode!=0,'mutation accepted '+name);controls.append({'case':name,'optimized':opt,'rejected':True})
  for name,fn in [('rehash_claim_inflation_internal_scope',scope),('rehash_proof_change_frozen_pin',resauthor)]:
   r=tmp/name;shutil.copytree(ROOT,r);fn(r);local=hashlib.sha256((r/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
   for opt in [False,True]:
    p=run(r,opt,local);need(p.returncode!=0,'resigned inner mutation accepted '+name);controls.append({'case':name,'optimized':opt,'rejected':True})
 need(all(j==clean[0] for j in clean),'normal/optimized/relocation mismatch');print(json.dumps({'status':'PASS','problem_id':6200061,'clean_runs':4,'publication_hostile_rejections':sum(x.get('rejected',False) for x in controls),'normalized_outputs_agree':True,'formal_proof':False,'general_problem_solved':False,'controls':controls},sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
