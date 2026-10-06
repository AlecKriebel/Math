#!/usr/bin/env python3
"""Publication-level normal/optimized relocation and negative inventory tests."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(value,message):
 if not value:raise RuntimeError(message)
def fp(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def run():
 source=Path(__file__).resolve().parent
 pins=json.loads((source/'PUBLICATION_CODE_PINS.json').read_text())['files']
 for name in ('verify_publication.py','test_publication.py'):
  require(fp((source/name).read_bytes())==pins[name],'initial code pin '+name)
 def execute(root,opt,quick=False):
  return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(root/'verify_publication.py')]+(['--integrity-only'] if quick else []),cwd='/tmp',capture_output=True,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 def remanifest(root,name):
  p=root/'PUBLICATION_MANIFEST.json';d=json.loads(p.read_text());d['files'][name]=fp((root/name).read_bytes());p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 results=[]
 with tempfile.TemporaryDirectory(prefix='exchangeable-publication-') as temp:
  temp=Path(temp);pristine=temp/'relocated publication with spaces';shutil.copytree(source,pristine)
  for opt in (False,True):
   r=execute(pristine,opt);require(r.returncode==0,'relocation '+r.stderr.decode());results.append({'test':'relocation','optimized':opt,'status':'PASS'})
  cases=['extra_file','extra_empty_directory','cache_directory','cache_regular_file','missing_file','modified_proof','extra_symlink','replaced_file_symlink','fifo','zip_changed_with_manifest_updated','wrapper_changed_with_manifest_updated','source_status_overclaim_with_manifest_updated','duplicate_manifest_key']
  for case in cases:
   root=temp/case;shutil.copytree(source,root)
   if case=='extra_file':(root/'EXTRA').write_text('unexpected')
   elif case=='extra_empty_directory':(root/'empty').mkdir()
   elif case=='cache_directory':(root/'__pycache__').mkdir()
   elif case=='cache_regular_file':(root/'__pycache__').write_text('cache')
   elif case=='missing_file':(root/'audit'/'INDEPENDENT_LEMMAS.md').unlink()
   elif case=='modified_proof':
    p=root/'author'/'PROOF.md';p.write_bytes(p.read_bytes()+b'\nmutation\n')
   elif case=='extra_symlink':(root/'LINK').symlink_to('README.md')
   elif case=='replaced_file_symlink':
    p=root/'author'/'PROOF.md';p.unlink();p.symlink_to(source/'author'/'PROOF.md')
   elif case=='fifo':os.mkfifo(root/'FIFO')
   elif case=='zip_changed_with_manifest_updated':
    n='archives/EXCHANGEABLE_FACTORIZATIONS_30001176_AUTHOR_SAFE_FREEZE.zip';p=root/n;p.write_bytes(p.read_bytes()+b'mutation');remanifest(root,n)
   elif case=='wrapper_changed_with_manifest_updated':
    n='verify_publication.py';p=root/n;p.write_bytes(p.read_bytes()+b'\n# mutation\n');remanifest(root,n)
   elif case=='source_status_overclaim_with_manifest_updated':
    n='VERDICT.json';p=root/n;d=json.loads(p.read_text());d['full_source_solved']=True;p.write_text(json.dumps(d));remanifest(root,n)
   elif case=='duplicate_manifest_key':
    p=root/'PUBLICATION_MANIFEST.json';p.write_text(p.read_text().replace('{','{"schema":1,',1))
   for opt in (False,True):
    r=execute(root,opt,True);require(r.returncode!=0 and b'FAIL:' in r.stderr,'accepted mutation '+case);results.append({'test':case,'optimized':opt,'status':'REJECTED'})
 return {'schema':1,'status':'PASS','positive_relocation_runs':2,'mutation_types_tested':len(cases),'mutation_runs_rejected':2*len(cases),'socket_fixture':'NOT_ATTEMPTED_BY_PUBLICATION_HARNESS; see preserved audit ENV_DENIED_NOT_RUN','scope':'Integrity diagnostics only; not a mathematical proof.','results':results}
if __name__=='__main__':
 try:print(json.dumps(run(),sort_keys=True,indent=2))
 except Exception as error:
  print('FAIL: '+str(error),file=sys.stderr);sys.exit(1)
