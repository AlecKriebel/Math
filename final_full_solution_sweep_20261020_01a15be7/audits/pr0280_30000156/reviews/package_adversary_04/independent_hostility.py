#!/usr/bin/env python3
"""Actual extracted verifier hostile copies, outputs in own ignored custody."""
from pathlib import Path
import shutil,json,tempfile,subprocess,sys,os
R=Path(__file__).resolve().parent;P=R.parents[3]/'private/pr0280_package_adversary_04';Z=P/'archive/birational-cycle-verification';out=[]
for mode in [[],['-O']]:
 for case in ['schema_true','schema_float','schema_string','schema_extra','bytes_true','bytes_float','duplicate','parent','backslash','missing','extra','symlink','manifest_symlink','fifo','false_baseline']:
  with tempfile.TemporaryDirectory(dir=P,prefix='hostile_') as t:
   q=Path(t)/'package';shutil.copytree(Z,q);mp=q/'MANIFEST.json';m=json.loads(mp.read_text());e=m['files'][0]
   if case=='schema_true':m['schema']=True
   elif case=='schema_float':m['schema']=1.0
   elif case=='schema_string':m['schema']='1'
   elif case=='schema_extra':m['extra']='unknown'
   elif case=='bytes_true':e['bytes']=True
   elif case=='bytes_float':e['bytes']=float(e['bytes'])
   elif case=='duplicate':m['files'].append(dict(e))
   elif case=='parent':e['path']='../outside'
   elif case=='backslash':e['path']='sub\\file'
   elif case=='missing':(q/e['path']).unlink()
   elif case=='extra':(q/'unreviewed.txt').write_text('extra')
   elif case=='symlink':
    f=q/e['path'];b=f.read_bytes();f.unlink();outside=Path(t)/'outside';outside.write_bytes(b);f.symlink_to(outside)
   elif case=='manifest_symlink':
    outside=Path(t)/'outside';outside.write_bytes(mp.read_bytes());mp.unlink();mp.symlink_to(outside)
   elif case=='fifo':os.mkfifo(q/'pipe')
   elif case=='false_baseline':
    import hashlib
    f=q/'expected_checks.json';v=json.loads(f.read_text());v['exact_checks']+=1;f.write_text(json.dumps(v));z=next(e for e in m['files'] if e['path']=='expected_checks.json');z['bytes']=f.stat().st_size;z['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
   if case!='manifest_symlink':mp.write_text(json.dumps(m))
   run=subprocess.run([sys.executable,'-B']+mode+[str(q/'verify.py')],capture_output=True,text=True,timeout=60)
   if run.returncode==0:raise RuntimeError('Unexpected acceptance '+case)
   out.append({'case':case,'optimized':bool(mode),'rejected':True,'stderr_last':run.stderr.splitlines()[-1]})
print(json.dumps({'all_reject':True,'runs':out},indent=2))
