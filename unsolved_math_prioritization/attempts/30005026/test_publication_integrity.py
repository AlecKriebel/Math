#!/usr/bin/env python3
"""Adversarial delivery-integrity controls; do not alter the original packet."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
import verify_publication as v
ROOT=Path(__file__).resolve().parent
def main():
 v.require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled')
 pin=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest();v.integrity(ROOT,pin)
 checks=[]
 def reject(label,mutation):
  with tempfile.TemporaryDirectory(prefix='coding-negative-') as td:
   p=Path(td)/'packet';shutil.copytree(ROOT,p);mutation(p)
   try: v.integrity(p,pin)
   except (ValueError,OSError): checks.append({'control':label,'rejected':True})
   else: raise ValueError('Mutation accepted: '+label)
 def changed(p,n): (p/n).write_bytes((p/n).read_bytes()+b'\n')
 reject('changed author proof',lambda p:changed(p,'author/RESULT.md'))
 reject('changed audit proof',lambda p:changed(p,'audit/AUDIT.md'))
 reject('changed source corrections',lambda p:changed(p,'SOURCE_CORRECTIONS.md'))
 reject('changed original ZIP encoding',lambda p:changed(p,'frozen_archives/'+v.SPECS[0][0]+'.b64'))
 reject('missing frozen member',lambda p:(p/'author/verify.py').unlink())
 reject('extra root file',lambda p:(p/'unexpected.txt').write_text('unexpected'))
 reject('extra nested file',lambda p:(p/'audit/unexpected.txt').write_text('unexpected'))
 reject('extra empty directory',lambda p:(p/'unexpected').mkdir())
 reject('symlink entry',lambda p:(p/'unexpected').symlink_to(p/'README.md'))
 reject('publication manifest tamper',lambda p:changed(p,'PUBLICATION_MANIFEST.json'))
 reject('frozen manifest tamper',lambda p:changed(p,'author/AUTHOR_MANIFEST.json'))
 for label,flags,env_extra in [('optimized interpreter',['-O'],{}),('optimization environment',[],{'PYTHONOPTIMIZE':'1'})]:
  env=dict(os.environ);env.update(env_extra);env['PYTHONDONTWRITEBYTECODE']='1'
  r=subprocess.run([sys.executable,*flags,'-B',str(ROOT/'verify_publication.py'),'--expected-manifest',pin],env=env,capture_output=True)
  v.require(r.returncode!=0 and b'Assertions must remain enabled' in r.stderr,label+' not rejected')
  checks.append({'control':label,'rejected':True})
 v.integrity(ROOT,pin)
 print(json.dumps({'status':'PASS','controls':checks,'controls_rejected':len(checks),'original_packet_unchanged':True},indent=2,sort_keys=True))
if __name__=='__main__': main()
