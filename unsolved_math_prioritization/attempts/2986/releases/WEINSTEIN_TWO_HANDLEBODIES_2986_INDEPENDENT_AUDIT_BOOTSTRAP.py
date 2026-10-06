#!/usr/bin/env python3
"""Verify the exact independently accepted safe audit ZIP before isolated replay.

Obtain the independent receipt and verify this bootstrap's own digest first.
Finite integrity/algebra checks are not mathematical proof certification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

BASE=Path(__file__).resolve().parent
ARCHIVE_NAME='WEINSTEIN_TWO_HANDLEBODIES_2986_INDEPENDENT_AUDIT_SAFE.zip'
MANIFEST_NAME='WEINSTEIN_TWO_HANDLEBODIES_2986_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
ARCHIVE_PIN=(42665,'33db9f07a08be710bf6479b572d509b44bf9dd499b02f6d01d75b3047cc90e2d')
MANIFEST_PIN=(2963,'66439c8c32ea34cafb654e91186d73cc93f322a980791abd901ea0bcd9782476')

def require(condition,message):
 if not condition:raise ValueError(message)

def digest(b):return hashlib.sha256(b).hexdigest()

def pin(data,expected,label):
 require(len(data)==expected[0],label+': byte count mismatch')
 require(digest(data)==expected[1],label+': hash mismatch')

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--archive',type=Path,default=BASE/ARCHIVE_NAME)
 p.add_argument('--external-manifest',type=Path,default=BASE/MANIFEST_NAME)
 p.add_argument('--corpus-dir',type=Path);p.add_argument('--source-dir',type=Path)
 a=p.parse_args()
 require(bool(a.corpus_dir)==bool(a.source_dir),'Supply both external input directories or neither')
 corpus=a.corpus_dir.resolve() if a.corpus_dir else None
 sources=a.source_dir.resolve() if a.source_dir else None
 ab=a.archive.read_bytes();mb=a.external_manifest.read_bytes()
 pin(ab,ARCHIVE_PIN,'audit archive');pin(mb,MANIFEST_PIN,'external audit manifest')
 ext=json.loads(mb)
 require(ext['archive']=={'name':ARCHIVE_NAME,'bytes':ARCHIVE_PIN[0],'sha256':ARCHIVE_PIN[1]},'wrong archive metadata')
 entries=ext['members'];expected={e['path']:e for e in entries}
 require(len(expected)==len(entries)==12,'wrong external member count')
 with zipfile.ZipFile(a.archive) as z:
  infos=z.infolist();names=[i.filename for i in infos]
  require(len(names)==len(set(names))==12,'duplicate/wrong ZIP members')
  require(set(names)==set(expected),'unexpected ZIP members')
  for i in infos:
   require(Path(i.filename).name==i.filename and not Path(i.filename).is_absolute() and not i.is_dir(),'unsafe ZIP path')
   require(not stat.S_ISLNK(i.external_attr>>16),'ZIP symlink')
   e=expected[i.filename];pin(z.read(i),(e['bytes'],e['sha256']),i.filename)
  results=[]
  for optimize in [False,True]:
   with tempfile.TemporaryDirectory(prefix='weinstein sealed audit relocation ') as td:
    dest=Path(td)/'accepted safe audit';dest.mkdir();z.extractall(dest)
    cmd=[sys.executable,'-I','-B']+(['-O'] if optimize else [])+[str(dest/'verify_audit.py')]
    if corpus:cmd+=['--corpus-dir',str(corpus),'--source-dir',str(sources)]
    r=subprocess.run(cmd,cwd=td,capture_output=True,text=True,timeout=120)
    require(r.returncode==0,'audit replay failed: '+r.stderr)
    require(not r.stderr,'unexpected replay stderr')
    result=json.loads(r.stdout)
    require(result['result']=='PASS' and result['formal_proof_certification'] is False,'wrong audit result')
    results.append(r.stdout)
  require(results[0]==results[1],'normal/optimized audit outputs differ')
 print(json.dumps({'result':'PASS','problem_id':2986,'decision':'accepted exact unchanged author archive as bounded partial, 4/5; unresolved','archive_sha256':ARCHIVE_PIN[1],'external_manifest_sha256':MANIFEST_PIN[1],'isolated_relocated_normal_and_optimized':True,'byte_identical_stdout':True,'audit_stdout_sha256':digest(results[0].encode()),'external_inputs_supplied':bool(corpus),'formal_proof_certification':False,'audit_result':json.loads(results[0])},indent=2,sort_keys=True))

if __name__=='__main__':
 try:main()
 except Exception as e:
  print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
