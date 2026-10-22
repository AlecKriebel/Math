#!/usr/bin/env python3
"""Replay only after separately pinned authentication; write only this review directory."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[1]/'work/pr872_revision_r1'
PORT=ROOT/'publication_20261015/verification_package'
EXPECTED={'verify_current_publication.py':'57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe','publication_20261015/preprint/build_verification.py':'94f3250eda9748d99353ac5339226ce3556cd9b7828a909a1fab2be318ef4404'}
for name,pin in EXPECTED.items():
 if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=pin:raise ValueError('external startup hash mismatch')
receipts=[]
for mode in ('normal','optimized'):
 flags=['-I','-S','-B']+(['-O'] if mode=='optimized' else [])
 jobs=[('outer_full',[str(ROOT/'verify_current_publication.py'),'02d511d2c24414615006dd1e97e134061c65888955f534c25d1c12e4edc4d8be','--root',str(ROOT),'--full']),('deterministic_rebuild',[str(ROOT/'publication_20261015/preprint/build_verification.py'),str(PORT),'09b94f08b7b30f4657bd0ed18f6c2ef86c58aec4ab1813badd12078c9cf36444','bf4b7f54267ec12bf3ed14bd8ae7410e2e3497943249bdc320bd8108fc9fc9aa',str(HERE/('rebuild_'+mode))])]
 for label,args in jobs:
  start=time.monotonic();p=subprocess.run([sys.executable,*flags,*args],cwd=HERE,capture_output=True,timeout=750)
  if p.returncode or p.stderr:raise ValueError((label,mode,p.returncode,p.stderr.decode(),p.stdout.decode()))
  data=json.loads(p.stdout)
  if data['status']!='PASS':raise ValueError('child status was not PASS')
  if label=='deterministic_rebuild' and not (data['sha256']=='c300b11741b2f8da35febe771114b5def4489bf91bf6d87d19debc5e6bc57731' and data['bytes']==453413):raise ValueError('rebuilt ZIP hash or size mismatch')
  (HERE/(label+'_'+mode+'.json')).write_bytes(p.stdout)
  receipts.append({'mode':mode,'label':label,'seconds':time.monotonic()-start,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()})
  print(label,mode,'PASS',flush=True)
(HERE/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
