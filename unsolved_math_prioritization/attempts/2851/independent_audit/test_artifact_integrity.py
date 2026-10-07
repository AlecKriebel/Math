#!/usr/bin/env python3
"""Adversarial pin-layer tests; all mutations take place in temporary copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 root=Path(__file__).resolve().parent
 names=['replay.py','AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json','independent_check.py','INDEPENDENT_RESULTS.json']
 tests=[]
 with tempfile.TemporaryDirectory(prefix='strong-heegaard-tamper-') as t:
  t=Path(t)
  for case in ['zip_byte_drift','zip_truncated','extra_zip_member','member_replacement','manifest_drift','independent_code_drift','independent_result_drift']:
   target=t/case;target.mkdir()
   for name in names:shutil.copyfile(root/name,target/name)
   z=target/'AUTHOR_SAFE_FREEZE.zip'
   if case=='zip_byte_drift':
    b=bytearray(z.read_bytes());b[-1]^=1;z.write_bytes(b)
   elif case=='zip_truncated':z.write_bytes(z.read_bytes()[:-1])
   elif case=='extra_zip_member':
    with zipfile.ZipFile(z,'a') as f:f.writestr('UNAPPROVED.txt','unapproved audit fixture')
   elif case=='member_replacement':
    with zipfile.ZipFile(z) as f:members={n:f.read(n) for n in f.namelist()}
    members['REPORT.md']+=b'\nAltered statement.\n'
    with zipfile.ZipFile(z,'w') as f:
     for n,b in members.items():f.writestr(n,b)
   else:
    file={'manifest_drift':'AUTHOR_EXTERNAL_MANIFEST.json','independent_code_drift':'independent_check.py','independent_result_drift':'INDEPENDENT_RESULTS.json'}[case]
    p=target/file;p.write_bytes(p.read_bytes()+b'\n')
   for mode in [[],['-O']]:
    p=subprocess.run([sys.executable]+mode+[str(target/'replay.py')],cwd=t,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    need(p.returncode==1 and p.stderr.startswith(b'REJECT: ') and not p.stdout,'integrity mutation accepted: '+case)
    tests.append({'case':case,'mode':'optimized' if mode else 'normal','exit_code':1,'stderr':p.stderr.decode().strip()})
 print(json.dumps({'status':'PASS_EXPLICIT_ARTIFACT_PIN_REJECTION','tests':tests,'count':len(tests),'original_archive_preserved':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
