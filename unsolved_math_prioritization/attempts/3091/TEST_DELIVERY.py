#!/usr/bin/env python3
"""Whole-delivery attacks using a fixed external entrypoint; outputs go only to stdout."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile

def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('delivery',type=Path);ap.add_argument('queue',type=Path);a=ap.parse_args();root=a.delivery.absolute();queue=a.queue.absolute();boot=root/'DELIVERY_BOOTSTRAP.py';results=[]
 before={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()};qbefore=sha(queue.read_bytes())
 def run(target,q,flags,cwd=None,env=None):
  p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(boot),str(target),'--queue',str(q),'--integrity-only'],cwd=cwd,env=env,capture_output=True,text=True,timeout=30)
  return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 def record(name,label,r,error=None):
  need((r['exit_code']==0 and r['stderr']=='') if error is None else (r['exit_code']==1 and r['stdout']=='' and r['stderr']=='REJECT: '+error+'\n'),'unexpected exact delivery outcome: '+name)
  results.append({'case':name,'mode':label,'expected_error':error,**r})
 modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
 with tempfile.TemporaryDirectory(prefix='hexagon-delivery-controls-') as td:
  temp=Path(td)
  for label,flags in modes:record('baseline',label,run(root,queue,flags))
  mutation_files={'acceptance':'ACCEPTANCE.md','outer-readme':'README.md','outer-evidence':'evidence/normal.stdout.json','outer-controls':'evidence/BOUNDARY_CONTROLS.json','expected-output-fixture':'packet/EXPECTED_OUTPUTS.json','inner-verifier':'packet/VERIFY_PUBLICATION.py','inner-bootstrap':'packet/BOOTSTRAP.py','outer-tests':'TEST_DELIVERY.py'}
  attacks=list(mutation_files)+['delivery-manifest','delivery-bootstrap','missing-acceptance','missing-evidence','extra-file','extra-directory','symlink-file','symlink-directory','fifo','wrong-queue','missing-queue','symlink-queue','repinned-attacker-tree']
  for name in attacks:
   d=temp/name;shutil.copytree(root,d)
   for p in [d,*d.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
   q=queue
   if name in mutation_files:
    n=mutation_files[name];p=d/n;p.write_bytes(p.read_bytes()+b'changed');error='delivery byte binding: '+n
   elif name=='delivery-manifest':
    p=d/'DELIVERY_MANIFEST.json';p.write_bytes(p.read_bytes()+b'\n');error='delivery manifest trust anchor'
   elif name=='delivery-bootstrap':
    p=d/'DELIVERY_BOOTSTRAP.py';p.write_bytes(p.read_bytes()+b'\n# changed\n');error='delivery bootstrap differs from trusted external copy'
   elif name=='missing-acceptance':(d/'ACCEPTANCE.md').unlink();error='delivery missing file: ACCEPTANCE.md'
   elif name=='missing-evidence':(d/'evidence/normal.stdout.json').unlink();error='delivery missing file: evidence/normal.stdout.json'
   elif name=='extra-file':(d/'extra.txt').write_text('unexpected');error='delivery file inventory mismatch'
   elif name=='extra-directory':(d/'extra-directory').mkdir();error='delivery directory inventory mismatch'
   elif name=='symlink-file':
    p=d/'ACCEPTANCE.md';p.unlink();p.symlink_to(root/'ACCEPTANCE.md');error='delivery symlink: ACCEPTANCE.md'
   elif name=='symlink-directory':shutil.rmtree(d/'evidence');(d/'evidence').symlink_to(root/'evidence',target_is_directory=True);error='delivery symlink: evidence'
   elif name=='fifo':os.mkfifo(d/'unexpected-fifo');error='delivery nonregular member: unexpected-fifo'
   elif name=='wrong-queue':q=temp/'wrong-QUEUE.md';q.write_bytes(queue.read_bytes()+b'changed');error='delivery queue binding'
   elif name=='missing-queue':q=temp/'absent-QUEUE.md';error='delivery queue input must be regular'
   elif name=='symlink-queue':q=temp/'symlink-QUEUE.md';q.symlink_to(queue);error='delivery queue input must be regular'
   elif name=='repinned-attacker-tree':
    p=d/'ACCEPTANCE.md';p.write_text('Invented acceptance.');manifest=d/'DELIVERY_MANIFEST.json';old=sha(manifest.read_bytes());m=json.loads(manifest.read_bytes())
    for row in m['files']:
     if row['path']=='ACCEPTANCE.md':row.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
    manifest.write_text(json.dumps(m));p=d/'DELIVERY_BOOTSTRAP.py';p.write_text(p.read_text().replace(old,sha(manifest.read_bytes())));error='delivery manifest trust anchor'
   for label,flags in modes:record(name,label,run(d,q,flags),error)
  hostile=temp/'hostile';hostile.mkdir();marker=temp/'EXECUTED'
  for n in ['json','hashlib','pathlib','subprocess','sitecustomize','usercustomize']:(hostile/(n+'.py')).write_text('open('+repr(str(marker))+',"w").write("bad")\nraise RuntimeError("hostile import")\n')
  env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'json.py'))
  for label,flags in modes:record('hostile-cwd-pythonpath',label,run(root,queue,flags,cwd=hostile,env=env))
  need(not marker.exists(),'hostile module executed')
 after={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
 need(before==after and sha(queue.read_bytes())==qbefore,'delivery or queue changed')
 print(json.dumps({'schema':'hexagon-entire-delivery-controls-v1','status':'PASS','external_bootstrap_sha256':sha(boot.read_bytes()),'delivery_manifest_sha256':sha((root/'DELIVERY_MANIFEST.json').read_bytes()),'precise_rejections':len(attacks)*3,'baseline_and_hostile_passes':6,'originals_unchanged':True,'results':results},sort_keys=True,indent=2))
if __name__=='__main__':main()
