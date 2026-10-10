#!/usr/bin/env python3
"""Public wrapper controls; authenticate this driver and the verifier externally first."""
import argparse, hashlib, json, os, runpy, shutil, stat, subprocess, sys, tempfile
from pathlib import Path

def need(ok,message):
 if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):
 return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(p.read_bytes()) if p.is_file() and not p.is_symlink() else None) for p in [root,*root.rglob('*')]}
def writable(root):
 root.chmod(0o755)
 for p in root.rglob('*'):
  if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--verifier-sha256',required=True);a=p.parse_args()
 need(os.getuid()!=0 and os.geteuid()!=0,'nonroot required');root=Path(__file__).absolute().parent;script=root/'verify_publication.py'
 need(sha(script.read_bytes())==a.verifier_sha256,'external verifier pin mismatch')
 api=runpy.run_path(str(script));api['verify'](root,a.manifest_sha256);before=snapshot(root)
 positives=[];negatives=[];schemas=[];denials=[];modes=['normal','-O','-OO']
 with tempfile.TemporaryDirectory(prefix='mesh-publication-controls-') as td:
  tmp=Path(td);poison=tmp/'poison';poison.mkdir();marker=tmp/'IMPORT_EXECUTED'
  for n in ['json.py','sitecustomize.py','fractions.py','hashlib.py']:(poison/n).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
  env=dict(os.environ);env['PYTHONPATH']=str(poison)
  def call(candidate,mode,pin=a.manifest_sha256,check=True):
   flags=[] if mode=='normal' else [mode]
   r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),'--packet',str(candidate),'--manifest-sha256',pin,*(['--check-only'] if check else [])],cwd=poison,env=env,capture_output=True,timeout=1200)
   need(not marker.exists(),'ambient hostile module executed');return r
  ro=tmp/'readonly';shutil.copytree(root,ro)
  for p in ro.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
  ro.chmod(0o555);ro_before=snapshot(ro)
  try:
   for label,path in [('create-root',ro/'probe'),('overwrite-existing',ro/'README.md'),('create-nested',ro/'original/freeze/packet/probe')]:
    try:
     with path.open('ab'):pass
    except PermissionError:denials.append(label)
    else:raise RuntimeError('read-only write succeeded: '+label)
   for mode in modes:
    for label,candidate in [('baseline',root),('readonly',ro)]:
     r=call(candidate,mode,check=False);need(r.returncode==0 and not r.stderr,label+' '+mode+': '+r.stderr.decode());result=api['load'](r.stdout)
     need(result['status']=='PASS' and result['check_only'] is False and len(result['replays'])==3,'incomplete positive replay');positives.append(label+' '+mode)
   need(snapshot(ro)==ro_before,'readonly snapshot changed')
  finally:writable(ro)
  cases=[]
  for path in sorted(api['FILES']|{'PUBLICATION_MANIFEST.json'}):
   cases.append(('byte-drift:'+path,lambda d,n=path:(d/n).write_bytes((d/n).read_bytes()+b'!')))
   cases.append(('missing:'+path,lambda d,n=path:(d/n).unlink()))
  cases += [('extra-file',lambda d:(d/'unexpected').write_text('x')),('extra-directory',lambda d:(d/'empty').mkdir()),('root-symlink',None)]
  def link(d):
   p=d/'README.md';p.unlink();p.symlink_to(root/'README.md')
  def fifo(d):
   p=d/'README.md';p.unlink();os.mkfifo(p)
  def hostile(d):
   (d/'original/freeze/packet/verify_math.py').write_text('from pathlib import Path\nPath('+repr(str(tmp/'EXECUTED'))+').write_text("bad")\n')
   mp=d/'PUBLICATION_MANIFEST.json';m=json.loads(mp.read_text())
   for e in m['files']:
    b=(d/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
   mp.write_text(json.dumps(m))
  cases += [('symlink-payload',link),('fifo-payload',fifo),('self-consistent-hostile-payload',hostile)]
  for i,(label,mutate) in enumerate(cases):
   d=tmp/('bad-'+str(i));shutil.copytree(root,d);writable(d)
   if mutate:mutate(d)
   else:
    linkpath=tmp/'linked-root';linkpath.symlink_to(d,target_is_directory=True);d=linkpath
   for mode in modes:
    r=call(d,mode);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'integrity control accepted: '+label+' '+mode);need(not (tmp/'EXECUTED').exists(),'hostile payload executed');negatives.append(label+' '+mode)
  d=tmp/'reanchored-hostile';shutil.copytree(root,d);writable(d);hostile(d)
  for mode in modes:
   r=call(d,mode,sha((d/'PUBLICATION_MANIFEST.json').read_bytes()));need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'reanchored hostile payload accepted');need(not (tmp/'EXECUTED').exists(),'hostile code executed');negatives.append('reanchored-hostile-payload '+mode)
  valid=json.loads((root/'PUBLICATION_MANIFEST.json').read_text());bodies=[]
  for key in ['problem_id','rank','new_mathematical_approaches']:
   for v in [True,False,float(valid[key]),str(valid[key]),None]:
    m=dict(valid);m[key]=v;bodies.append((key+':'+repr(v),json.dumps(m)))
  for v in [True,1.0,-1,'1',None]:
   m=json.loads(json.dumps(valid));m['files'][0]['bytes']=v;bodies.append(('bytes:'+repr(v),json.dumps(m)))
  for field in ['zero_outputs_allowed','formal_proof_claimed','source_files_redistributed']:
   m=dict(valid);m[field]=int(valid[field]);bodies.append((field,json.dumps(m)))
  m=dict(valid);m['files']=valid['files']+[valid['files'][0]];bodies.append(('duplicate-path',json.dumps(m)))
  for badpath in ['../outside','/absolute','a//b','a/./b','a/../b','a\\b']:
   m=json.loads(json.dumps(valid));m['files'][0]['path']=badpath;bodies.append(('unsafe-path:'+badpath,json.dumps(m)))
  bodies += [('duplicate-json-key','{"rank":1030,"rank":1030}'),('nan','{"rank":NaN}'),('infinity','{"rank":Infinity}'),('overflow','{"rank":1e999}'),('malformed','{bad'),('list','[]')]
  for i,(label,body) in enumerate(bodies):
   d=tmp/('schema-'+str(i));shutil.copytree(root,d);writable(d);mp=d/'PUBLICATION_MANIFEST.json';mp.write_text(body);pin=sha(mp.read_bytes())
   for mode in modes:
    r=call(d,mode,pin);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'schema accepted: '+label+' '+mode);schemas.append(label+' '+mode)
  for mode in modes:
   r=call(root,mode,'0'*64);need(r.returncode==1,'wrong external pin accepted');negatives.append('wrong-external-pin '+mode)
  need(snapshot(root)==before,'original packet changed')
 return {'schema':'mesh-preserver-publication-controls-v1','status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'modes':modes,'positive_replays':len(positives),'integrity_rejections':len(negatives),'reanchored_schema_rejections':len(schemas),'actual_readonly_write_denials':denials,'ambient_hostile_imports_executed':False,'bytes_and_inventory_unchanged':True,'positives':positives,'integrity_cases':negatives,'schema_cases':schemas}
if __name__=='__main__':
 try:print(json.dumps(main(),sort_keys=True,indent=2))
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
